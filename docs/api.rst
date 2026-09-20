Code Reference
==============

This section documents the core modules of the synchrotron motion simulator.

BasicFunc Module
----------------

``BasicFunc.py`` contains all physics functions used by the simulation scripts.
It reads parameters from ``Input.py`` and defines the following:

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

Input Module
------------

``Input.py`` is a plain Python file that serves as the configuration for all
simulation scripts. It contains no functions; all parameters are defined as
module-level variables. See the :doc:`usage` section for a complete description
of each parameter.
