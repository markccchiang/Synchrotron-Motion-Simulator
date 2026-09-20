Code Reference
==============

This section documents the core modules of the synchrotron motion simulator.

BasicFunc Module
----------------

``src/BasicFunc.py`` contains all physics functions used by the simulation scripts.
It reads parameters from ``src/Input.py`` and defines the following:

Physical Constants
^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 25 40 25

   * - Variable
     - Description
     - Value
   * - ``c_speed``
     - Speed of light (m/s)
     - :math:`2.998 \times 10^8`
   * - ``e_mass``
     - Electron mass (kg)
     - :math:`9.109 \times 10^{-31}`
   * - ``p_mass``
     - Proton mass (kg)
     - :math:`1.673 \times 10^{-27}`
   * - ``e_charge``
     - Elementary charge (C)
     - :math:`1.602 \times 10^{-19}`
   * - ``C_gamma_e``
     - Electron radiation coefficient (m/eV\ :sup:`3`)
     - :math:`8.846 \times 10^{-32}`
   * - ``C_gamma_p``
     - Proton radiation coefficient (m/eV\ :sup:`3`)
     - :math:`7.783 \times 10^{-45}`

Energy Functions
^^^^^^^^^^^^^^^^

``KE(t)``
   Returns the kinetic energy at time *t* during the ramping cycle.

   .. math::

      K(t) = \frac{K_f - K_i}{2}\left[\frac{K_f + K_i}{K_f - K_i}
             - \cos(2\pi f t)\right]

``E_total_p(t)``
   Total energy for a proton: :math:`E = m_p c^2 + eK(t)`.

``E_total_e(t)``
   Total energy for an electron: :math:`E = m_e c^2 + eK(t)`.

RF Voltage Function
^^^^^^^^^^^^^^^^^^^

``V_RF(t)``
   Returns the RF voltage at time *t* using the smooth adiabatic ramp model:

   .. math::

      V(t) = \left[3\left(\frac{t}{T_\nu}\right)^2
             - 2\left(\frac{t}{T_\nu}\right)^3\right](V_f - V_i) + V_i
      \quad \text{for } 0 \le t \le T_\nu

Relativistic Functions
^^^^^^^^^^^^^^^^^^^^^^

``gamma_e(E)`` / ``gamma_p(E)``
   Lorentz factor: :math:`\gamma = E / (m_0 c^2)`.

``beta2_e(E)`` / ``beta2_p(E)``
   Velocity parameter squared: :math:`\beta^2 = 1 - 1/\gamma^2`.

``v_e(E)`` / ``v_p(E)``
   Particle velocity: :math:`v = \beta c`.

Lattice Functions
^^^^^^^^^^^^^^^^^

``eta_e(E)`` / ``eta_p(E)``
   Slip factor: :math:`\eta = \alpha_c - 1/\gamma^2`.

``nu_s_e(E, V)`` / ``nu_s_p(E, V)``
   Synchrotron frequency parameter:
   :math:`\nu_s = \sqrt{h|\eta|eV / (2\pi\beta^2 E)}`.

``Q_s_e(E, V, t)`` / ``Q_s_p(E, V, t)``
   Synchrotron tune: :math:`Q_s = \nu_s \sqrt{|\cos\phi_s|}`.

``T_s_e(E, V, t)`` / ``T_s_p(E, V, t)``
   Synchrotron period: :math:`T_s = T_0 / Q_s`.

``alpha_ad_e(E, V, t)`` / ``alpha_ad_p(E, V, t)``
   Adiabatic coefficient:
   :math:`\alpha_\text{ad} = |dT_s/dt| / (2\pi)`.

``area_e(E, V, t)`` / ``area_p(E, V, t)``
   Bucket area approximation.

Revolution Period Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^

``period_e(E)`` / ``period_p(E)``
   Revolution period: :math:`T_0 = L / v`.

``t_e_new(t, E)`` / ``t_p_new(t, E)``
   Time at the next turn: :math:`t_{n+1} = t_n + T_0`.

``t_e_old(t, E)`` / ``t_p_old(t, E)``
   Time at the previous turn: :math:`t_{n-1} = t_n - T_0`.

Phase Factor Functions
^^^^^^^^^^^^^^^^^^^^^^

``U0_e(E)`` / ``U0_p(E)``
   Energy radiated per turn by the synchronous particle, in joules:
   :math:`U_0 = e\,C_\gamma E^4 / \rho`. Because :math:`C_\gamma` is quoted
   in m/eV\ :sup:`3`, *E* is converted to eV inside these functions; the result
   is returned in joules to match :math:`\Delta E`.

``phis_e(t, E)`` / ``phis_p(t, E)``
   Synchronous phase. The synchronous particle must supply both the ramp energy
   gain and the energy it radiates each turn:

   .. math::

      \phi_s = \sin^{-1}\left[\frac{K(t_{n+1}) - K(t_n) + U_0/e}{V}\right]

Tracking Iteration Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``iteration_e(delta_E, phi, t, E)`` / ``iteration_p(delta_E, phi, t, E)``
   Core phase-space mapping step. Given the current energy deviation
   :math:`\Delta E`, phase :math:`\phi`, time *t*, and total energy *E*,
   returns the updated :math:`(\Delta E_{n+1},\ \phi_{n+1})`:

   .. math::

      \Delta E_{n+1} &= \Delta E_n + eV(\sin\phi_n - \sin\phi_s)
                        - \left[U_0(E + \Delta E_n) - U_0(E)\right] \\
      \phi_{n+1} &= \phi_n + \frac{2\pi h \eta}{\beta^2 E} \Delta E_{n+1}

   The synchronous particle's own radiation loss is already balanced by
   :math:`\phi_s`, so what acts on the deviation is the *excess* this particle
   radiates over the synchronous one. That difference vanishes at
   :math:`\Delta E = 0` and, to first order, equals
   :math:`4 U_0 \Delta E / E` — the usual radiation damping term.

Separatrix Search
^^^^^^^^^^^^^^^^^

``envelope_e(t, num_of_turns, Delta_rad=ENVELOPE_DELTA_RAD)`` / ``envelope_p(...)``
   Trace the RF bucket boundary at ramping time *t*, returning
   ``(phi, Delta_E/E)`` for electrons and ``(phi, Delta_P/P)`` for protons.

   The search steps the starting phase inward from ``ENVELOPE_PHI_E``
   (:math:`2\pi`) or ``ENVELOPE_PHI_P`` (:math:`\pi`) in steps of *Delta_rad*
   until the trajectory stays bounded. Those starting values set both the
   launch point and the escape threshold, so changing them moves every
   published envelope.

   The search is capped at one full RF period, :math:`\lfloor 2\pi /
   \Delta_{rad} \rfloor`, and raises ``RuntimeError`` if no starting phase
   yields a bounded trajectory — beyond that sweep there is nothing left to
   find, and without the cap the loop would spin forever.

``ENVELOPE_DELTA_RAD``
   Phase step of the search, 0.01 rad. Against 0.001 this costs 0.076 % in
   bucket height for a ten times cheaper search.

Vectorised Bunch Tracking
^^^^^^^^^^^^^^^^^^^^^^^^^

The scalar functions above are the reference implementation and are what the
batch scripts use. These are elementwise twins for tracking a whole bunch at
once, used by the interactive UI.

They are exact rather than approximate: :math:`V_{RF}(t)`, :math:`\phi_s`,
:math:`\eta`, :math:`\beta^2` and :math:`U_0` depend only on the per-turn
scalars *(t, E)* that every particle shares, so :math:`\Delta E` and
:math:`\phi` are the only array quantities. Substituting ``numpy.sin`` for
``math.sin`` over the same operation order reproduces the scalar map
bit-for-bit, at roughly sixty times the speed.

``iteration_e_vec(delta_E, phi, t, E)`` / ``iteration_p_vec(...)``
   Elementwise twin of ``iteration_e`` / ``iteration_p``; *delta_E* and *phi*
   are arrays.

``bunch_init_e(num_of_particles, sigma_dPoP, mean_dPoP, ...)`` / ``bunch_init_p(...)``
   Initial bunch: Gaussian in :math:`\Delta E/E` (electrons) or
   :math:`\Delta P/P` (protons, carrying the extra :math:`\beta^2`), flat in
   phase over :math:`[0, 2\pi]` for electrons and :math:`[-\pi, +\pi]` for
   protons. Seeded with the same values the batch scripts use, so results match
   them exactly.

``track_turns_e(delta_E, phi, t, E, num_of_turns)`` / ``track_turns_p(...)``
   Advance the bunch, returning ``(delta_E, phi, t, E)`` as the batch scripts
   would record it at that turn index — that is, before the next kick.

``capture_rate(dPoP, phi, range_dPoP, range_phi1, range_phi2)``
   Percentage of the bunch inside the survival window. *dPoP* is
   :math:`\Delta E/E` for electrons and :math:`\Delta P/P` for protons; the
   caller applies the :math:`\beta^2`.

Runtime Configuration
^^^^^^^^^^^^^^^^^^^^^

``BasicFunc`` snapshots ``Input`` at import time, but its functions look those
names up at call time, so assigning to them takes effect immediately. This is
what lets the UI vary parameters without rewriting ``src/Input.py`` or
reloading the module.

``CONFIG_NAMES``
   The names that may be overridden: ``E_min``, ``E_max``, ``f``, ``L``,
   ``alpha_c``, ``rho``, ``V_min``, ``V_max``, ``T_nu``, ``h``.

   Note that ``f`` is the ramping frequency here, which collides with the
   conventional ``import BasicFunc as f`` alias.

``snapshot()``
   Current value of every configuration name, for display or restore.

``override(**kwargs)``
   Set configuration values for subsequent calls, returning the previous ones
   so the caller can restore them. Every name is validated before anything is
   assigned: a partial apply followed by a raise would leave a mutated global
   behind with no way for the caller to know what to restore.

Input Module
------------

``src/Input.py`` is a plain Python file that serves as the configuration for all
simulation scripts. It contains no functions; all parameters are defined as
module-level variables. See the :doc:`usage` section for a complete description
of each parameter.
