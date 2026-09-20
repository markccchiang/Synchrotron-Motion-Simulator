<p align="center">
  <img src="assets/logo-wordmark.svg" width="360" alt="Synchrotron Motion Simulator">
</p>

A Python-based simulator for synchrotron longitudinal beam dynamics during booster ramping cycles. It models RF capture, phase-space evolution, and particle tracking for both proton and electron beams.

**Author:** Cheng-Chin (C.C.) Chiang (2014)

## Overview

This tool simulates the longitudinal motion of charged particles in a synchrotron booster ring. It supports:

- Plotting energy, RF voltage, and other ramping parameters over a full cycle
- Computing and visualizing the RF bucket (separatrix) envelope in phase space
- Single-particle tracking through the ramping cycle
- Multi-particle tracking with capture efficiency calculation
- Animated visualizations of phase-space evolution (exported as `.mp4`)
- An interactive browser UI for tuning the RF ramp against capture efficiency

The physics and mathematical formulations are documented in [`notes/MarkCCChiang-note.pdf`](notes/MarkCCChiang-note.pdf).

## Requirements

- **Python** >= 3.12
- **NumPy**
- **Matplotlib** >= 1.2
- **FFmpeg** (for generating animation videos)

## Setup

There is no package metadata, so a plain virtual environment is all that is
needed. Using [uv](https://docs.astral.sh/uv/):

```bash
uv venv --python 3.12             # creates .venv/
uv pip install numpy matplotlib
```

Then either activate the environment:

```bash
source .venv/bin/activate         # Windows: .venv\Scripts\activate
```

or skip activation and call the interpreter directly, e.g.
`.venv/bin/python examples/track-electron.py`.

FFmpeg is not a Python package and must be installed separately — `brew install
ffmpeg` on macOS, `apt install ffmpeg` on Debian/Ubuntu. It is only required by the
`*-animation-*.py` scripts.

## Project Structure

The physics module and its configuration live in `src/`; the runnable
scripts live in `examples/`. Each script imports `_srcpath` first, which puts
`src/` on `sys.path`, so a bare `python examples/<script>.py` works from any
working directory. Output files are written to the current directory.

| File | Description |
|------|-------------|
| `examples/_srcpath.py` | Puts `src/` on `sys.path` for the scripts |
| `src/Input.py` | User-configurable parameters (beam energy, RF settings, etc.) |
| `src/BasicFunc.py` | Core physics functions (energy, RF, tracking iterations) |
| `examples/plot-{proton,electron}.py` | Plot ramping parameters (energy, voltage, frequency, etc.) |
| `examples/envelope-{proton,electron}.py` | Compute the phase-space envelope at a given time |
| `examples/envelope-animation-{proton,electron}.py` | Animate the envelope over the ramping cycle |
| `examples/track-{proton,electron}.py` | Single-particle phase-space tracking |
| `examples/track-animation{1,2,3}-{proton,electron}.py` | Animated multi-particle tracking |
| `examples/track-multiparticle-{proton,electron}.py` | Multi-particle tracking with capture efficiency output |
| `examples/plot-eff-vs-time-{proton,electron}.py` | Plot capture efficiency vs. time |
| `examples/plot-phase-space-{proton,electron}.py` | Plot phase-space snapshots |
| `examples/ui.py`, `examples/ui.html` | Interactive capture-optimisation UI |
| `src/Input.py.example-proton` | Example input parameters for proton simulation |
| `src/Input.py.example-electron` | Example input parameters for electron simulation |

## Usage

### 1. Configure input parameters

Copy one of the example configuration files to `src/Input.py`:

```bash
# For proton simulation
cp src/Input.py.example-proton src/Input.py

# For electron simulation
cp src/Input.py.example-electron src/Input.py
```

Edit `src/Input.py` to adjust beam energy, RF voltage, harmonic number, and other parameters as needed.

### 2. Run the simulation scripts

Run these from the repository root. The explicit interpreter path needs no
activation; if you activated the environment instead (see [Setup](#setup)), plain
`python` works in its place.

**Proton simulation:**

```bash
.venv/bin/python examples/plot-proton.py                 # Plot ramping parameters
.venv/bin/python examples/envelope-proton.py             # Phase-space envelope
.venv/bin/python examples/envelope-animation-proton.py   # Envelope animation  -> envelope-animation-proton.mp4
.venv/bin/python examples/track-proton.py                # Single-particle tracking
.venv/bin/python examples/track-animation1-proton.py     # Tracking animation 1 -> track-animation1-proton.mp4
.venv/bin/python examples/track-animation2-proton.py     # Tracking animation 2 -> track-animation2-proton.mp4
.venv/bin/python examples/track-animation3-proton.py     # Tracking animation 3 -> track-animation3-proton.mp4
.venv/bin/python examples/track-multiparticle-proton.py  # Multi-particle stats  -> eff-proton.dat
.venv/bin/python examples/plot-eff-vs-time-proton.py     # Plot efficiency data
.venv/bin/python examples/plot-phase-space-proton.py     # Phase-space snapshot
```

**Electron simulation:**

```bash
.venv/bin/python examples/plot-electron.py                 # Plot ramping parameters
.venv/bin/python examples/envelope-electron.py             # Phase-space envelope
.venv/bin/python examples/envelope-animation-electron.py   # Envelope animation  -> envelope-animation-electron.mp4
.venv/bin/python examples/track-electron.py                # Single-particle tracking
.venv/bin/python examples/track-animation1-electron.py     # Tracking animation 1 -> track-animation1-electron.mp4
.venv/bin/python examples/track-animation2-electron.py     # Tracking animation 2 -> track-animation2-electron.mp4
.venv/bin/python examples/track-animation3-electron.py     # Tracking animation 3 -> track-animation3-electron.mp4
.venv/bin/python examples/track-multiparticle-electron.py  # Multi-particle stats  -> eff-electron.dat
.venv/bin/python examples/plot-eff-vs-time-electron.py     # Plot efficiency data
.venv/bin/python examples/plot-phase-space-electron.py     # Phase-space snapshot
```

## Interactive UI

For exploring capture efficiency, `examples/ui.py` serves a browser UI on localhost:

```bash
.venv/bin/python examples/ui.py          # opens a tab at http://127.0.0.1:8000
.venv/bin/python examples/ui.py --species proton --port 8080 --no-browser
```

Drag the RF voltages, capture time, harmonic number or bunch spread and the phase-space
plot and capture rate update live. Switch between **electron** and **proton** with the
toggle at the top of the panel; each species brings its own survival window, plot limits
and phase convention. The species it opens with follows `src/Input.py`, or `--species`.

All physics runs in `BasicFunc` on the Python side — the page only draws — so the UI and
the batch scripts cannot drift apart. It uses the vectorised `iteration_*_vec` map, which
reproduces the scalar map bit-for-bit while running ~60x faster.

## Documentation

Full documentation (theory, optimization results, code reference) is available
as a Sphinx project under the `docs/` directory. To build it:

```bash
uv pip install -r docs/requirements.txt
cd docs
make html
```

The generated HTML will be at `docs/_build/html/index.html`.

## License

ISC License. See [LICENSE.md](LICENSE.md) for details.
