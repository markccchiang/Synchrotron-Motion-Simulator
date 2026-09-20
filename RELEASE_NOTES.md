# Release Notes

## v0.0

First tagged release of the Synchrotron Motion Simulator — the 2014 TLS booster
study code, brought up to date and made runnable on a current Python toolchain.

The physics is unchanged from the original work; this release is about making that
work reproducible by someone other than its author.

### Simulation core

- **Python 3 support.** All `print` statements converted to function calls across
  18 files. The code previously ran only under Python 2.
- **Errors are raised, not returned.** `V_RF()`, `beta2_e()` and `beta2_p()` used to
  return an error *string* on invalid input, which then propagated into arithmetic
  and surfaced as a confusing `TypeError` several frames away. They now raise
  `ValueError` with the offending value.
- **`phis_p()` / `phis_e()` always return a value.** The previous `if`/`elif` chain
  could fall through and return `None` for a NaN argument. The synchronous phase is
  now clamped into the valid `asin` domain.
- **Fixed a copy-paste bug in `track-electron.py`**, which initialised its energy and
  β² from the *proton* functions (`E_total_p`, `beta2_p`). Electron tracking results
  before this fix were wrong.
- **LaTeX axis labels are raw strings.** Literals such as `'$\phi$'` and
  `'$\Delta E / E$'` contain invalid Python escape sequences; these are
  `SyntaxWarning` as of Python 3.12 and are slated to become errors.
- **Corrected the `C_gamma_p` comment** (`7.783e-32` → `7.783e-45`) to match the value
  actually used in the code.

### Documentation

- **Sphinx documentation** under `docs/`, transcribing the theory, the derivations and
  the optimization study from `Documentation/MarkCCChiang-note.pdf` into
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

The **electron** configuration (`Input.py.example-electron`) was run end to end on
Python 3.12.12 with NumPy 2.5.3 and Matplotlib 3.11.2. All ten scripts complete:

| Check | Result |
|---|---|
| Ramping cycle | 208151 turns, 0.0500 s — exactly the half-period of the 10 Hz ramp |
| Capture efficiency | 99.9%, consistent across all three multi-particle scripts |
| Figures | 9 `.eps` files, matching the committed set in `TLS-booster-figure/` |
| Animations | 4 `.mp4` files, valid H.264, frame counts matching the configured turns |

### Known limitations

- **The proton configuration was not re-verified for this release.** Only the electron
  path has been run end to end since the Python 3 migration.
- **`Input.py` is tracked in git** and must be overwritten to switch species, so
  selecting a beam dirties the working tree. It currently holds the electron values.
- **Config cannot be overridden via `PYTHONPATH`.** Because every script does
  `import Input as para`, and Python places the *script's* directory at `sys.path[0]`,
  an alternate `Input.py` elsewhere on the path is silently ignored. To run a variant,
  copy the script next to the alternate config.
- **`envelope-animation-*.py` and `track-animation3-*.py` are slow** — roughly 37 and
  23 minutes respectively. Both redo the full separatrix search once per frame with
  `Delta_rad = 0.001`, ten times finer than the standalone `envelope-*.py` uses. The
  other animation scripts finish in about a minute.
- **The physics functions are scalar.** `BasicFunc` uses `math`, not NumPy ufuncs, so
  multi-particle scripts loop per particle and cannot be vectorized as written.
- `docs/conf.py` still declares `release = '1.0'`, which does not match this tag.

### Requirements

Python >= 3.12, NumPy, Matplotlib >= 1.2, and FFmpeg for the animation scripts.
See the README for setup.
