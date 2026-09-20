#!/usr/bin/env python
"""Interactive capture-optimisation UI.

Serves examples/ui.html and a small JSON API on localhost. All physics runs in
BasicFunc on this side; the browser only draws. Nothing is reimplemented in
JavaScript, so there is one source of truth for the simulation.

    python examples/ui.py                # opens a browser tab
    python examples/ui.py --species proton --port 8080 --no-browser
"""
import argparse
import json
import os
import sys
import threading
import traceback
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

import numpy as np

import _srcpath # noqa: F401 - puts ../src on sys.path
import BasicFunc as func
import Input as para

HERE = os.path.dirname(os.path.abspath(__file__))

# Per-species wiring. The only real differences are which _p/_e functions to
# call and whether the vertical coordinate carries the beta^2 that turns
# Delta_E/E into Delta_P/P -- the same split the batch scripts have.
SPECIES = {
    'electron': dict(
        label='electron', axis='&Delta;E / E',
        E_total=lambda t: func.E_total_e(t),
        bunch_init=lambda n, s, m: func.bunch_init_e(n, s, m),
        track=lambda dE, phi, t, E, n: func.track_turns_e(dE, phi, t, E, n),
        envelope=lambda t, n: func.envelope_e(t, n),
        phis=lambda t, E: func.phis_e(t, E),
        Qs=lambda E, V, t: func.Q_s_e(E, V, t),
        area=lambda E, V, t: func.area_e(E, V, t),
        scale=lambda E: 1.0,
    ),
    'proton': dict(
        label='proton', axis='&Delta;P / P',
        E_total=lambda t: func.E_total_p(t),
        bunch_init=lambda n, s, m: func.bunch_init_p(n, s, m),
        track=lambda dE, phi, t, E, n: func.track_turns_p(dE, phi, t, E, n),
        envelope=lambda t, n: func.envelope_p(t, n),
        phis=lambda t, E: func.phis_p(t, E),
        Qs=lambda E, V, t: func.Q_s_p(E, V, t),
        area=lambda E, V, t: func.area_p(E, V, t),
        scale=lambda E: func.beta2_p(E),
    ),
}


def defaults(species):
    # Starting point for the sliders: whatever src/Input.py currently holds.
    cfg = func.snapshot()
    return {
        'species': species,
        'axis': SPECIES[species]['axis'],
        'config': cfg,
        'bunch': {
            'num_of_particles': para.num_of_particles,
            'sigma_dPoP': para.sigma_dPoP,
            'mean_dPoP': para.mean_dPoP,
            'num_of_turns': para.app5_num_of_turns,
        },
        'window': {
            'range_dPoP': para.range_dPoP,
            'range_phi1': para.range_phi1,
            'range_phi2': para.range_phi2,
        },
        'limits': {
            'xlim': [para.set_xlim1, para.set_xlim2],
            'ylim': [para.set_ylim1, para.set_ylim2],
        },
    }


def thin(values, most):
    # Keep the payload small without changing what the curve looks like.
    values = np.asarray(values)
    if len(values) <= most:
        return values
    return values[:: int(np.ceil(len(values)/most))]


def simulate(req):
    sp = SPECIES[req.get('species', 'electron')]
    bunch = req['bunch']
    window = req['window']

    previous = func.override(**req['config'])
    try:
        n = int(bunch['num_of_particles'])
        turns = int(bunch['num_of_turns'])
        dE, phi = sp['bunch_init'](n, float(bunch['sigma_dPoP']),
                                   float(bunch['mean_dPoP']))
        t, E = 0.0, sp['E_total'](0.0)
        dE, phi, t, E = sp['track'](dE, phi, t, E, turns)

        dPoP = dE/E/sp['scale'](E)
        capture = func.capture_rate(dPoP, phi, float(window['range_dPoP']),
                                    float(window['range_phi1']),
                                    float(window['range_phi2']))

        sep_phi, sep_dPoP = sp['envelope'](t, int(req.get('separatrix_turns', 1000)))
        V = func.V_RF(t)
        return {
            'phi': [round(float(x), 4) for x in phi],
            'dPoP': [round(float(x)*100.0, 4) for x in dPoP],
            'separatrix': {
                'phi': [round(float(x), 4) for x in thin(sep_phi, 900)],
                'dPoP': [round(float(x)*100.0, 4) for x in thin(sep_dPoP, 900)],
            },
            'capture': round(capture, 2),
            'phis_deg': round(np.degrees(sp['phis'](t, E)), 4),
            'Qs': float('%.6g' % sp['Qs'](E, V, t)),
            'area': float('%.6g' % sp['area'](E, V, t)),
            'V_RF': round(V, 2),
            'KE_MeV': round(func.KE(t)/1.0e6, 4),
            'time_ms': round(t*1000.0, 5),
            'turns': turns,
        }
    finally:
        # Always restore, so one bad request cannot poison later ones.
        func.override(**previous)


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, payload, content_type='application/json'):
        body = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
        self.send_response(code)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ('/', '/index.html'):
            with open(os.path.join(HERE, 'ui.html'), 'rb') as fh:
                self._send(200, fh.read(), 'text/html; charset=utf-8')
        elif self.path.startswith('/api/defaults'):
            species = 'proton' if 'proton' in self.path else self.server.species
            self._send(200, defaults(species))
        else:
            self._send(404, {'error': 'not found'})

    def do_POST(self):
        if self.path != '/api/simulate':
            self._send(404, {'error': 'not found'})
            return
        try:
            length = int(self.headers.get('Content-Length', 0))
            req = json.loads(self.rfile.read(length) or b'{}')
        except ValueError as exc:
            self._send(400, {'error': 'bad request: %s' % exc})
            return
        try:
            self._send(200, simulate(req))
        except (KeyError, TypeError) as exc:
            # a malformed request, not a physics outcome
            self._send(400, {'error': str(exc).strip('"')})
        except (ValueError, RuntimeError) as exc:
            # An unphysical slider position is an expected outcome, not a crash:
            # phis_* raises when the RF cannot supply the ramp, envelope_* when
            # the separatrix search will not converge. Report it as text.
            self._send(200, {'error': str(exc)})
        except Exception:
            traceback.print_exc()
            self._send(500, {'error': 'internal error; see the server log'})

    def log_message(self, fmt, *args):
        pass # the default logs every request; too noisy while dragging a slider


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--port', type=int, default=8000)
    ap.add_argument('--species', choices=sorted(SPECIES), default=None,
                    help='default species (guessed from src/Input.py if omitted)')
    ap.add_argument('--no-browser', action='store_true')
    args = ap.parse_args()

    # Input.py comments its ranges per species; a negative lower phi limit is
    # the proton convention ([-pi, pi]) and 0 the electron one ([0, 2*pi]).
    species = args.species or ('proton' if para.range_phi1 < 0 else 'electron')

    # Single-threaded on purpose: requests serialise, so the module-level config
    # that override() mutates cannot be raced between two simulations.
    server = HTTPServer(('127.0.0.1', args.port), Handler)
    server.species = species
    url = 'http://127.0.0.1:%d/' % args.port

    print('Synchrotron capture-optimisation UI')
    print('  species : %s (from src/Input.py)' % species)
    print('  serving : %s' % url)
    print('  stop    : Ctrl-C')
    if not args.no_browser:
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nstopped')
        server.server_close()


if __name__ == '__main__':
    main()
