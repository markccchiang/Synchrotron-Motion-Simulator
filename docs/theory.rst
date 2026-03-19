Evolution of Synchrotron Phase-Space Ellipse
=============================================

The RF cavity is operated in a resonance condition to provide accelerating
voltage, i.e. longitudinal electric field, to particles. For simplicity, we do
not consider the effects of synchro-betatron coupling. The synchrotron equations
of motion can be derived from the Hamiltonian. For beam acceleration, it is
suitable to choose the phase-space mapping equation in the coordinates
:math:`(\phi, \Delta E)`, where :math:`\phi` is the phase of RF voltage and
:math:`\Delta E` is the change of a particle energy per revolution.

Phase-Space Mapping Equations
-----------------------------

Let :math:`n` be the turn number for a particle in a ring accelerator. The
evolution equations of synchrotron motion in phase-space
:math:`(\phi, \Delta E)` are:

.. math::

   \Delta E_{n+1} = \Delta E_n + eV(\sin\phi_n - \sin\phi_s)
                    - C_\gamma \frac{E^4}{\rho}

.. math::

   \phi_{n+1} = \phi_n + \frac{2\pi h \eta}{\beta^2 E} \Delta E_{n+1}

where the auxiliary quantities are defined as:

.. math::

   eV \sin\phi_s &= E(t_{n+1}) - E(t_n) \\
   \gamma &= \frac{E}{m_0 c^2} \\
   \beta &= \sqrt{1 - \frac{1}{\gamma^2}} \\
   v &= \beta c \\
   \eta &= \alpha_c - \frac{1}{\gamma^2} \\
   \frac{\Delta E}{\beta^2 E} &= \frac{\Delta P}{P}

Symbol Definitions
^^^^^^^^^^^^^^^^^^

- :math:`e` -- particle charge
- :math:`V` -- RF voltage
- :math:`E` -- total energy of a particle
- :math:`\rho` -- local radius of curvature of a bending magnet
- :math:`h` -- harmonic number for RF
- :math:`\phi_s` -- phase factor for RF
- :math:`m_0` -- stationary mass of a particle
- :math:`c` -- speed of light
- :math:`v` -- particle velocity
- :math:`\alpha_c` -- momentum compaction factor for a ring accelerator
- :math:`P` -- momentum of a particle

Radiation Power Coefficient
---------------------------

The radiation power coefficient :math:`C_\gamma` is deduced from Larmor's
theorem, which depends on the particle type:

.. math::

   C_\gamma = \frac{4\pi}{3} \frac{r_0}{(m_0 c^2)^3}

.. math::

   C_\gamma =
   \begin{cases}
   8.846 \times 10^{-5} \text{ m/(GeV)}^3 & \text{for electrons} \\
   7.783 \times 10^{-18} \text{ m/(GeV)}^3 & \text{for protons}
   \end{cases}

where :math:`r_0 = e^2 / 4\pi\epsilon_0 m_0 c^2` is the classical radius for a
particle.

RF Voltage Model
----------------

The RF voltage :math:`V` as a function of time in a ramping cycle is modeled as:

.. math::

   V(t) =
   \begin{cases}
   \left[3\left(\dfrac{t}{T_\nu}\right)^2
   - 2\left(\dfrac{t}{T_\nu}\right)^3\right] (V_f - V_i) + V_i
   & \text{for } 0 \le t \le T_\nu \\[6pt]
   V_f & \text{for } t > T_\nu
   \end{cases}

where :math:`T_\nu` is the adiabatic capture time, and :math:`V_i` and
:math:`V_f` are initial and final RF voltages, respectively. The setting of
:math:`T_\nu` affects the efficiency for adiabatic capture.

Kinetic Energy as a Function of Time
-------------------------------------

The total energy :math:`E` and kinetic energy :math:`K` as functions of time
in a ramping cycle are:

.. math::

   E(t) = m_0 c^2 + K(t)

.. math::

   K(t) = \left(\frac{K_f - K_i}{2}\right)
          \left[\frac{K_f + K_i}{K_f - K_i} - \cos(2\pi f t)\right]

where :math:`K(t)` is the kinetic energy obtained from RF voltage, :math:`K_i`
and :math:`K_f` are initial and final kinetic energies for a particle in a
ramping cycle, and :math:`f` is the booster ramping frequency.

Bending Magnetic Field
^^^^^^^^^^^^^^^^^^^^^^

The bending magnetic field for a booster ring as a function of time,
:math:`B(t)`, should be cooperated with :math:`K(t)` in order to keep particles
in the same orbit:

.. math::

   E(t)^2 = m_0^2 c^4 + P(t)^2 c^2

.. math::

   B(t) = \frac{P(t)}{e\rho}
        = \frac{1}{e\rho} \frac{\sqrt{E(t)^2 - m_0^2 c^4}}{c^2}

RF Phase Factor
---------------

For a particle with a small stationary mass or very high kinetic energy compared
to :math:`m_0 c^2`, the :math:`B(t)` is approximately proportional to
:math:`K(t)`. From the mapping equations, the change of total energy for a
particle per revolution is equal to the change of kinetic energy:

.. math::

   eV \sin\phi_s = E(t_{n+1}) - E(t_n) = K(t_{n+1}) - K(t_n)

where :math:`t_{n+1} - t_n` is the revolution period for a particle between
turn :math:`n` and :math:`n+1`:

.. math::

   t_{n+1} - t_n = \frac{L}{v(E(t_n))}

:math:`L` is the circumference of the ring accelerator. The RF phase factor
:math:`\phi_s` is thus:

.. math::

   \phi_s = \sin^{-1}\left[\frac{K(t_{n+1}) - K(t_n)}{eV}\right]

Note that this equation also sets the maximum rate for the ramping of kinetic
energy with :math:`0 \le |K(t_{n+1}) - K(t_n)| < eV`.

Synchrotron Tune and Adiabatic Coefficient
------------------------------------------

The synchrotron tune :math:`Q_s` is calculated by

.. math::

   Q_s = \nu_s \sqrt{|\cos\phi_s|}, \quad \text{where } \nu_s
       = \sqrt{\frac{h|\eta|eV}{2\pi\beta^2 E}}

if :math:`\eta \neq 0`. The adiabatic coefficient :math:`\alpha_\text{ad}` is
then defined as

.. math::

   \alpha_\text{ad} = \frac{1}{2\pi}\left|\frac{dT_s}{dt}\right|,
   \quad \text{where } T_s = T_0 / Q_s

:math:`T_0` is the revolution period. The condition for adiabatic synchrotron
motion is :math:`\alpha_\text{ad} \ll 1`.

Bucket Area
-----------

The phase-space area enclosed by the separatrix is called bucket area,
:math:`\tilde{A}_\text{B}`, which is approximated as

.. math::

   \tilde{A}_\text{B} \approx \frac{16 Q_s}{h|\eta|\sqrt{|\cos\phi_s|}}
   \left(\frac{1 - \sin\phi_s}{1 + \sin\phi_s}\right)

Since bucket area is the maximum size of a beam we can make, we should avoid
the zero bucket area with :math:`\phi_s = 90°` from the phase factor equation.
