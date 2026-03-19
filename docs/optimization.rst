Optimize the TLS Booster as a Proton or Electron Machine
=========================================================

Fixed Parameters
----------------

For the TLS booster, the fixed parameters are:

.. list-table::
   :header-rows: 1
   :widths: 40 30

   * - Parameter
     - Value
   * - Circumference :math:`L`
     - 72 m
   * - Bending radius :math:`\rho`
     - 5 m
   * - Momentum compaction :math:`\alpha_c`
     - 0.1346
   * - Initial kinetic energy :math:`K_i`
     - 7 MeV
   * - Final kinetic energy :math:`K_f`
     - 300 MeV
   * - Ramping frequency :math:`f`
     - 10 Hz

For the RF cavity, the fixed parameters are :math:`h = 2` and
:math:`V_f = 15` kV.

The RF voltage variables :math:`T_\nu` and :math:`V_i` are crucial parameters
to be optimized for the best efficiency of adiabatic capture.

Initial Beam Conditions
-----------------------

We assume the initial conditions for a bunch of the beam is flatly distributed
in the phase:

- :math:`\phi = [-\pi,\ \pi]` (rad) for protons
- :math:`\phi = [0,\ 2\pi]` (rad) for electrons

and the distribution of :math:`\Delta P/P` (for protons) or
:math:`\Delta E/E` (for electrons) is a Gaussian with zero mean and
:math:`\sigma = \pm 0.05\%` or :math:`\sigma = \pm 0.5\%`, i.e., the width of
:math:`\Delta P/P` (:math:`\Delta E/E`) is 0.1% or 1%.

Two thousand particles (:math:`N = 2000`) are generated to represent a bunch of
the beam. We track these particles by the synchrotron motion simulator and
obtain the capture efficiency for particles in a ramping cycle.

Ramping Cycle Duration
----------------------

For protons (electrons) acceleration, it takes about 95,500 (208,151) turns to
accomplish a ramping cycle.

Best RF Voltage Settings
------------------------

The following table lists the RF voltage settings with :math:`T_\nu` and
:math:`V_i` for the best efficiencies of TLS booster as a proton or electron
accelerator, and with different initial beam distributions :math:`\Delta P/P` or
:math:`\Delta E/E`.

.. list-table::
   :header-rows: 1
   :widths: 35 15 15 20

   * - Beam type (initial Gaussian width)
     - :math:`T_\nu` (ms)
     - :math:`V_i` (kV)
     - Efficiency (%)
   * - protons (:math:`\Delta P/P = 0.1\%`)
     - 0.5
     - 7.5
     - :math:`99 \pm 2.2^*`
   * - protons (:math:`\Delta P/P = 1\%`)
     - 0.1
     - 7
     - :math:`85.7 \pm 2.2^*`
   * - electrons (:math:`\Delta E/E = 0.1\%`)
     - 0.1
     - 12.5
     - :math:`99.9 \pm 2.2^*`
   * - electrons (:math:`\Delta E/E = 1\%`)
     - 0.1
     - 12
     - :math:`98 \pm 2.2^*`

:math:`^*` The standard error :math:`= \sqrt{N}/N`, where :math:`N = 2000`
is the total number of particles in simulation.

Proton Optimization
-------------------

The scan ranges are :math:`T_\nu = [0.1,\ 4.9]` (ms) and
:math:`V_i = [0.5,\ 15]` (kV). The properties of adiabatic capture for TLS
booster as a proton machine are characterized by:

- Particle velocity :math:`v/c` vs. time
- RF phase factor :math:`\phi_s` vs. time
- RF voltage :math:`V` vs. time
- Adiabatic coefficient :math:`\alpha_\text{ad}` vs. time
- Synchrotron tune :math:`Q_s` vs. time
- Bucket area :math:`\tilde{A}_\text{B}` vs. time

With optimal settings (:math:`T_\nu = 0.5` ms, :math:`V_i = 7.5` kV), the
proton capture efficiency reaches approximately 99% for a beam with
:math:`\Delta P/P = 0.1\%`.

Electron Optimization
---------------------

Similarly, the electron optimization uses the same scan ranges. With optimal
settings (:math:`T_\nu = 0.1` ms, :math:`V_i = 12.5` kV), the electron
capture efficiency reaches approximately 99.9% for a beam with
:math:`\Delta E/E = 0.1\%`.

The electrons acceleration usually has a better efficiency compared to protons
or other heavy particles.

Summary of Findings
-------------------

- For **protons** acceleration, it is better to have the initial beam condition
  with a small :math:`\Delta P/P` distribution and a small adiabatic capture
  time :math:`T_\nu` for RF voltage setting, in order to have the best
  efficiency.

- For **electrons** acceleration, the requirements for good capture efficiency
  are roughly the same as with protons. However, the electron acceleration
  usually has a better efficiency compared to protons or other heavy particles.
