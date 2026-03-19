Usage
=====

Requirements
------------

- **Python** >= 3.12
- **NumPy**
- **Matplotlib** >= 1.2
- **FFmpeg** (for generating animation videos)

Configuration
-------------

Before running any simulation, copy one of the example configuration files to
``Input.py``:

.. code-block:: bash

   # For proton simulation
   cp Input.py.example-proton Input.py

   # For electron simulation
   cp Input.py.example-electron Input.py

Edit ``Input.py`` to adjust the following parameters:

Booster Ramping Scenario
^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 20 50 20

   * - Parameter
     - Description
     - Example
   * - ``E_min``
     - Initial kinetic energy (eV)
     - ``7.0e+6``
   * - ``E_max``
     - Final kinetic energy (eV)
     - ``300.0e+6``
   * - ``f``
     - Booster ramping frequency (Hz)
     - ``10.0``
   * - ``L``
     - Circumference of the booster (m)
     - ``72.0``
   * - ``alpha_c``
     - Momentum compaction factor
     - ``0.1346``
   * - ``rho``
     - Local radius of curvature (m)
     - ``5.0``

RF Ramping Settings
^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 20 50 20

   * - Parameter
     - Description
     - Example
   * - ``V_min``
     - Initial RF voltage (V)
     - ``12.5e+3``
   * - ``V_max``
     - Final RF voltage (V)
     - ``15.0e+3``
   * - ``T_nu``
     - Adiabatic capture time (s)
     - ``0.1e-3``
   * - ``h``
     - Harmonic number of the RF
     - ``2.0``

Beam Distribution Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 25 50 15

   * - Parameter
     - Description
     - Example
   * - ``num_of_particles``
     - Number of particles for tracking
     - ``2000``
   * - ``sigma_dPoP``
     - Sigma of :math:`\Delta P/P` or :math:`\Delta E/E`
     - ``0.0005``
   * - ``mean_dPoP``
     - Mean of :math:`\Delta P/P` or :math:`\Delta E/E`
     - ``0.0``

Simulation Scripts
------------------

The simulator provides several applications, each available for both proton
and electron simulations. Replace ``{particle}`` with ``proton`` or
``electron`` below.

Application 0: Plot Ramping Parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   python plot-{particle}.py

Plots the kinetic energy, RF voltage, and other ramping parameters over a
full cycle. Also reports the total number of turns and total ramping time.

Application 1: Phase-Space Envelope
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   python envelope-{particle}.py

Computes the phase-space envelope (separatrix) at a specified time point.
Configure with ``app1_set_t`` and ``app1_num_of_turns`` in ``Input.py``.

Application 2: Envelope Animation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   python envelope-animation-{particle}.py

Produces an animated video (``envelope-animation-{particle}.mp4``) showing the
evolution of the phase-space envelope over the ramping cycle. Configure with
``app2_*`` parameters in ``Input.py``.

Application 3: Single-Particle Tracking
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   python track-{particle}.py

Tracks a single particle through the phase space for a complete ramping cycle.
Configure with ``app3_num_of_turns`` in ``Input.py``.

Application 4: Multi-Particle Tracking Animations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   python track-animation1-{particle}.py   # phase-space animation
   python track-animation2-{particle}.py   # time-domain animation
   python track-animation3-{particle}.py   # animation with envelope overlay

Tracks a bunch of particles and produces animated videos (``*.mp4``). Configure
with ``app4_num_of_turns`` in ``Input.py``.

Application 5: Capture Efficiency Calculation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   python track-multiparticle-{particle}.py

Tracks a bunch of particles and outputs the capture efficiency data to
``eff-{particle}.dat``. Configure with ``app5_num_of_turns`` in ``Input.py``.

Application 6: Efficiency vs. Time Plot
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   python plot-eff-vs-time-{particle}.py

Reads the data file ``eff-{particle}.dat`` produced by Application 5 and plots
the capture efficiency as a function of time.

Application 7: Phase-Space Snapshot
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   python plot-phase-space-{particle}.py

Plots a phase-space snapshot at a specific turn in the ramping cycle. Configure
with ``app7_num_of_turns`` in ``Input.py``.
