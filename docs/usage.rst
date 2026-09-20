Usage
=====

Requirements
------------

- **Python** >= 3.12
- **NumPy**
- **Matplotlib** >= 1.2
- **FFmpeg** (for generating animation videos)

Environment Setup
-----------------

The project is a flat collection of scripts with no package metadata, so a plain
virtual environment is all that is needed. Using `uv <https://docs.astral.sh/uv/>`_:

.. code-block:: bash

   uv venv --python 3.12
   uv pip install numpy matplotlib

Then either activate the environment with ``source .venv/bin/activate``, or call
the interpreter directly with its full path, as shown below.

FFmpeg is not a Python package and must be installed separately (``brew install
ffmpeg`` on macOS, ``apt install ffmpeg`` on Debian/Ubuntu). It is only required
by the ``*-animation-*.py`` scripts.

Configuration
-------------

Before running any simulation, copy one of the example configuration files to
``src/Input.py``:

.. code-block:: bash

   # For proton simulation
   cp src/Input.py.example-proton src/Input.py

   # For electron simulation
   cp src/Input.py.example-electron src/Input.py

Edit ``src/Input.py`` to adjust the following parameters:

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

   .venv/bin/python examples/plot-{particle}.py

Plots the kinetic energy, RF voltage, and other ramping parameters over a
full cycle. Also reports the total number of turns and total ramping time.

Application 1: Phase-Space Envelope
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   .venv/bin/python examples/envelope-{particle}.py

Computes the phase-space envelope (separatrix) at a specified time point.
Configure with ``app1_set_t`` and ``app1_num_of_turns`` in ``src/Input.py``.

Application 2: Envelope Animation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   .venv/bin/python examples/envelope-animation-{particle}.py

Produces an animated video (``envelope-animation-{particle}.mp4``) showing the
evolution of the phase-space envelope over the ramping cycle. Configure with
``app2_*`` parameters in ``src/Input.py``.

Application 3: Single-Particle Tracking
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   .venv/bin/python examples/track-{particle}.py

Tracks a single particle through the phase space for a complete ramping cycle.
Configure with ``app3_num_of_turns`` in ``src/Input.py``.

Application 4: Multi-Particle Tracking Animations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   .venv/bin/python examples/track-animation1-{particle}.py   # phase-space animation
   .venv/bin/python examples/track-animation2-{particle}.py   # time-domain animation
   .venv/bin/python examples/track-animation3-{particle}.py   # animation with envelope overlay

Tracks a bunch of particles and produces animated videos (``*.mp4``). Configure
with ``app4_num_of_turns`` in ``src/Input.py``.

Application 5: Capture Efficiency Calculation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   .venv/bin/python examples/track-multiparticle-{particle}.py

Tracks a bunch of particles and outputs the capture efficiency data to
``eff-{particle}.dat``. Configure with ``app5_num_of_turns`` in ``src/Input.py``.

Application 6: Efficiency vs. Time Plot
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   .venv/bin/python examples/plot-eff-vs-time-{particle}.py

Reads the data file ``eff-{particle}.dat`` produced by Application 5 and plots
the capture efficiency as a function of time.

Application 7: Phase-Space Snapshot
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   .venv/bin/python examples/plot-phase-space-{particle}.py

Plots a phase-space snapshot at a specific turn in the ramping cycle. Configure
with ``app7_num_of_turns`` in ``src/Input.py``.


Interactive UI
--------------

``examples/ui.py`` serves a browser UI for exploring capture efficiency:

.. code-block:: bash

   .venv/bin/python examples/ui.py
   .venv/bin/python examples/ui.py --species proton --port 8080 --no-browser

Dragging the RF voltages, capture time, harmonic number or bunch spread updates the
phase-space plot and the capture rate live. The Electron/Proton toggle at the top of
the panel switches species; each brings its own survival window, plot limits and phase
convention. The species the page opens with follows ``src/Input.py``, or ``--species``.

All physics runs in ``BasicFunc``; the page only draws. The UI uses the vectorised
``iteration_e_vec`` / ``iteration_p_vec`` map, which reproduces the scalar map
bit-for-bit at roughly sixty times the speed.
