# Release Notes

## v0.1

A correctness release. **Synchrotron radiation was silently absent from every
electron run before this version** — if you have electron results from v0.0, they
were produced by a machine that did not radiate. See below for what changed and
by how much.

### Corrected physics

- **Synchrotron radiation was computed in the wrong units and vanished.**
  `C_gamma_e` / `C_gamma_p` are quoted in m/eV³, but `iteration_e()` /
  `iteration_p()` passed them a total energy in **joules**. The loss term came out
  2.4 × 10⁵⁶ times too small — 9.5 × 10⁻⁷⁴ against a true 144.3 eV per turn at
  300 MeV — so radiation damping never acted.

  New `U0_e()` / `U0_p()` convert to eV internally and return joules. `U0_e` now
  matches the textbook `88.46 keV · E[GeV]⁴ / ρ` to zero relative error.

- **The synchronous phase now accounts for the radiated energy.** `phis_e()` /
  `phis_p()` previously solved `sin φs = ΔK/V`, balancing only the ramp gain. The
  synchronous particle must also replace what it radiates each turn, so the
  relation is now `sin φs = (ΔK + U₀/e)/V`. Fixing the loss term without this
  would have left the bunch sitting at the wrong phase.

- **Radiation enters the deviation equation as an excess, not a full loss.**
  Since `φs` now carries the synchronous particle's own loss, what acts on `ΔE`
  is `U₀(E + ΔE) − U₀(E)` — the difference that damps the oscillation. It
  vanishes exactly at `ΔE = 0` and matches the standard `4U₀ΔE/E` to first order.

**Impact.** Cumulative radiated energy over one ramp is 8.3 MeV, 2.8% of the
300 MeV beam. A particle launched at `ΔE/E = +0.3%` now ends a full 208151-turn
ramp at **−0.115%** instead of **+0.400%**; φs at extraction moves from 0.053° to
0.604°.

**The published capture-efficiency figures are unaffected.** Those runs cover
2000 turns at ~7 MeV, where U₀ is 5.6 × 10⁻⁵ eV — six orders of magnitude below
anything that matters. Electron and proton capture remain 99.9% and 99.0%, and
`eff-electron.dat` / `eff-proton.dat` are byte-identical to v0.0.

### Reliability

- **Unphysical configurations are reported instead of masked.** `phis_*` clamped
  its `asin` argument to ±0.9999. When the RF cannot supply the ramp that
  argument exceeds 1, meaning no synchronous particle and no bucket exist — but
  clamping reported φs ≈ 90° and let the run continue producing plausible-looking
  output. It now raises `ValueError` naming the time, the demand in eV per turn
  and the available voltage. Both shipped configs are far clear of the boundary:
  the argument peaks at 0.148 (electron) and 0.333 (proton).
- **The separatrix search is bounded.** It incremented without limit and could
  spin forever on a configuration with no bounded trajectory. It is now capped at
  one full RF period, `int(2π/Delta_rad)`, and raises with the ramp time and a
  pointer at the RF settings.
- **`plot-*.py` checks its array bound** instead of running for minutes and then
  raising `IndexError` past the fixed 10⁶ preallocation.

### Performance

Results are byte-identical across all of these.

| Script | v0.0 | v0.1 |
|---|---|---|
| `envelope-animation` | 2222 s (37 min) | **279 s (4.6 min)** |
| `track-animation3` | ~1400 s (23 min) | **197 s (3.3 min)** |
| `track-multiparticle` | 19.8 s | **10.7 s** |
| `track-animation2` | ~60 s | **17.4 s** |

- **One shared machine clock.** `var_t`, `var_E` and `var_beta2` were
  per-particle arrays whose entries were provably always identical — `var_E[j]`
  derives only from `var_t[j]`, never from the particle's own `ΔE`. The inner
  loop called `t_*_new`, `E_total_*` and `beta2_*` once per particle per turn to
  compute a single number. They are now scalars advanced once per turn.
- **One separatrix search.** Four scripts carried their own copy, disagreeing on
  the phase step (0.01 vs 0.001) and the turn count (`app2_num_of_turns` vs a
  hardcoded 3000), so "the envelope at time *t*" differed by which script drew
  it. `envelope_p()` / `envelope_e()` in `BasicFunc` replace all four. The step is
  settled at 0.01, which costs 0.076% in bucket height against 0.001 for a 10×
  cheaper search, and remains a keyword argument.

`track-animation1` is unchanged at ~55 s; its cost is matplotlib frame
rendering, not the physics loop.

### Project structure

- Code is split into `src/` (physics module and configuration) and `examples/`
  (the twenty runnable scripts). `BasicFunc` imports `Input` at module load, so
  the two must share a path entry — hence `Input.py` living beside it rather than
  with the scripts. Each script imports `_srcpath` first, so a bare
  `python examples/track-electron.py` works from any directory.
- `Documentation/` renamed to `notes/`, which no longer collides with the Sphinx
  `docs/`.
- `README.usage` removed; it was superseded by `README.md` and every path in it
  had become wrong.
- 25 write-only assignments removed, located by an AST scan.

### Verification

Both species run end to end on Python 3.12.12, NumPy 2.5.3, Matplotlib 3.11.2.
The proton configuration — untested in v0.0 — completes at 95500 turns and 99.0%
capture. Animation frame counts and durations are unchanged (501 / 25.05 s,
2001 / 57.17 s, 301 / 12.04 s).

### Known limitations

- **The physics functions are scalar.** `BasicFunc` uses `math`, not NumPy
  ufuncs, so multi-particle scripts still loop per particle.
- **`src/Input.py` is tracked in git** and must be overwritten to switch species,
  so selecting a beam dirties the working tree. It currently holds the electron
  values.
- **An alternate config cannot be supplied via `PYTHONPATH`.** `_srcpath` inserts
  `src/` at the front of `sys.path`, so `src/Input.py` always wins. To run a
  variant, copy the `src/` tree and edit the copy.
- **The radiation term is quartic in `ΔE`.** For a particle far outside the
  bucket it can overflow; this needs an absurd configuration (|ΔE| ~ 10⁷⁷ eV
  against a realistic peak of 0.07·E) and fails loudly rather than silently.
- Nothing in the repository is git-tagged yet.

---

## v0.0

First release of the Synchrotron Motion Simulator — the 2014 TLS booster study
code, brought up to date and made runnable on a current Python toolchain.

The physics is unchanged from the original work; this release is about making
that work reproducible by someone other than its author.

> **Note:** several items below were superseded in v0.1. They are kept as a
> record of what v0.0 actually was. Paths are written in their current form so
> the links resolve.

### Simulation core

- **Python 3 support.** All `print` statements converted to function calls across
  18 files. The code previously ran only under Python 2.
- **Errors are raised, not returned.** `V_RF()`, `beta2_e()` and `beta2_p()` used to
  return an error *string* on invalid input, which then propagated into arithmetic
  and surfaced as a confusing `TypeError` several frames away. They now raise
  `ValueError` with the offending value.
- **`phis_p()` / `phis_e()` always return a value.** The previous `if`/`elif` chain
  could fall through and return `None` for a NaN argument. The synchronous phase
  was clamped into the valid `asin` domain. *(Superseded in v0.1: the clamp was
  itself masking unphysical configurations, and now raises instead.)*
- **Fixed a copy-paste bug in `track-electron.py`**, which initialised its energy and
  β² from the *proton* functions (`E_total_p`, `beta2_p`). Electron tracking results
  before this fix were wrong.
- **LaTeX axis labels are raw strings.** Literals such as `'$\phi$'` and
  `'$\Delta E / E$'` contain invalid Python escape sequences; these are
  `SyntaxWarning` as of Python 3.12 and are slated to become errors.
- **Corrected the `C_gamma_p` comment** (`7.783e-32` → `7.783e-45`) to match the value
  actually used in the code. *(The coefficient was right; v0.1 found that the code
  using it was feeding it the wrong units.)*

### Documentation

- **Sphinx documentation** under `docs/`, transcribing the theory, the derivations and
  the optimization study from `notes/MarkCCChiang-note.pdf` into
  `introduction`, `theory`, `optimization`, `usage`, `api` and `references` pages.
- **Rewritten README** with a project-structure table and per-script usage.
- **Environment setup documented** for [uv](https://docs.astral.sh/uv/), in both the
  README and the Sphinx usage page.
- `docs/requirements.txt` records the Sphinx build dependency.

### Project setup

- **Project logo** (`assets/logo.svg`, `assets/logo-wordmark.svg`) built from the
  booster ring, the accelerating RF bucket separatrix and a captured bunch at the
  synchronous phase. Used in the README header and the Sphinx sidebar.
- `.gitignore` for build output, editor state and virtualenvs.
- ISC license.

### Verification

The **electron** configuration (`src/Input.py.example-electron`) was run end to end on
Python 3.12.12 with NumPy 2.5.3 and Matplotlib 3.11.2. All ten scripts complete:

| Check | Result |
|---|---|
| Ramping cycle | 208151 turns, 0.0500 s — exactly the half-period of the 10 Hz ramp |
| Capture efficiency | 99.9%, consistent across all three multi-particle scripts |
| Figures | 9 `.eps` files, matching the committed set in `TLS-booster-figure/` |
| Animations | 4 `.mp4` files, valid H.264, frame counts matching the configured turns |

### Known limitations

- **The proton configuration was not re-verified for this release.** Only the electron
  path had been run end to end since the Python 3 migration. *(Resolved in v0.1:
  95500 turns, 99.0% capture.)*
- **`Input.py` is tracked in git** and must be overwritten to switch species, so
  selecting a beam dirties the working tree.
- **Config cannot be overridden via `PYTHONPATH`,** because Python places the
  *script's* directory at `sys.path[0]`. *(Still true in v0.1, but for a different
  reason — see that section.)*
- **`envelope-animation-*.py` and `track-animation3-*.py` are slow** — roughly 37 and
  23 minutes respectively. Both redo the full separatrix search once per frame with
  `Delta_rad = 0.001`, ten times finer than the standalone `envelope-*.py` uses.
  *(Resolved in v0.1: 4.6 and 3.3 minutes.)*
- **The physics functions are scalar.** `BasicFunc` uses `math`, not NumPy ufuncs, so
  multi-particle scripts loop per particle and cannot be vectorized as written.

### Requirements

Python >= 3.12, NumPy, Matplotlib >= 1.2, and FFmpeg for the animation scripts.
See the README for setup.
