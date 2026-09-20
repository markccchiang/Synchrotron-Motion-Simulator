#////////////////////////////////////////////////////////////////////////////////////////////////////
#
# input the booster ramping scenario 
#
E_min = 7.0e+6 # initial kinetic energy of a particle (V), example: 7 (MeV)
E_max = 300.0e+6 # final kinetic energy of a particle (V), example: 300 (MeV)
f = 10.0 # booster ramping frequency (Hz), example: 10 (Hz)
L = 72.0 # circumference of the booster (m), example: 72 (m)
alpha_c = 0.1346 # momentum compaction factor of the booster, example: 0.1346
rho = 5.0 # local radius of curvature for an accelerator ring (m), example: 5 (m)
#////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////
#
# input the RF ramping settings
#
V_min = 12.5e+3 # initial RF voltage (V), example: 12.5 (kV)
V_max = 15.0e+3 # final RF voltage (V), example: 15 (kV)
T_nu = 0.1e-3 # adiabatic capture time (s), example: 0.1 (ms)
h = 2.0 # harmonic number of the RF, example: 2
#////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////
#
# set the mean and sigma of a bunch of beam
#
num_of_particles = 2000 # set no. of particles of a beam for tracking
sigma_dPoP = 0.0005 # set the sigma of (+/-) Delta_P/P for protons (Delta_E/E for electrons)
mean_dPoP = 0.0 # set the mean of (+/-) Delta_P/P for protons (Delta_E/E for electrons)
#////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////
#
# define the survival ranges
#
#range_dPoP = 0.02 # define the survival range of (+/-) Delta_P/P for protons 
#range_phi1 = -3.15 # define the lower limit of survival range phi (rad) for protons
#range_phi2 = 3.15 # define the upper limit of survival range phi (rad) for protons
#////////////////////////////////////////////////////////////////////////////////////////////////////
range_dPoP = 0.08 # define the survival range of (+/-) Delta_E/E for electrons
range_phi1 = 0.0 # define the lower limit of survival range phi (rad) for electrons
range_phi2 = 3.15*2 # define the upper limit of survival range phi (rad) for electrons
#////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////
#
# set the plot ranges
#
#set_xlim1 = -3.15 # set the lower limit of y-axis for a plot (rad): for proton
#set_xlim2 = 3.15 # set the upper limit of y-axis for a plot (rad): for proton
#set_ylim1 = -2.0 # set the lower limit of y-axis for a plot (%): for proton
#set_ylim2 = 2.0 # set the upper limit of y-axis for a plot (%): for proton
#////////////////////////////////////////////////////////////////////////////////////////////////////
set_xlim1 = 0.0 # set the lower limit of x-axis for a plot (rad): for electron
set_xlim2 = 3.15*2 # set the upper limit of x-axis for a plot (rad): for electron
set_ylim1 = -8.0 # set the lower limit of y-axis for a plot (%): for electron
set_ylim2 = 8.0 # set the upper limit of y-axis for a plot (%): for electron
#////////////////////////////////////////////////////////////////////////////////////////////////////





#////////////////////////////////////////////////////////////////////////////////////////////////////
#
# Application 0: [plot-proton.py & plot-electron.py]
#                plot the setting results and get the total number of turns for a ramping cycle 
#
#////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////
#
# Application 1: [envelope-proton.py & envelope-electron.py] 
#                check the envelope of phase space 
#
app1_set_t = 1.0e-3 # (s) set the ramping time point to get the envelope, example: 1.0e-3 (s)
app1_num_of_turns = 3000 # set the number of turns for tracking
#////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////
#
# Application 2: [envelope-animation-proton.py & envelope-animation-electron.py]
#                check the animation of the envelope in phase space
#
app2_set_start_t = 0.0 # set the start time (s)
app2_set_final_t = 0.050 # set the final time (s)
app2_num_of_turns = 3000 # set the number of turns for tracking
app2_num_of_intervals = 500 # no. of plots to show in the animation
#////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////
#
# Application 3: [track-proton.py & track-electron.py]
#                track a particle in phase space for a ramping cycle
#
app3_num_of_turns = 95500 # total number of turns for a ramping cycle (95500/208151 for protons/electrons)
#////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////
#
# Application 4: [track-animation1-proton.py & track-animation1-electron.py]
#                [track-animation2-proton.py & track-animation2-electron.py]
#                [track-animation3-proton.py & track-animation3-electron.py]
#                track a bunch of particles in phase space
#
app4_num_of_turns = 2000 # track no. of turns (2000/95500 for protons) (2000/208151 for electrons)
#////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////
#
# Application 5: [track-multiparticle-proton.py & track-multiparticle-electron.py]
#                track a bunch of particles in phase space
#
app5_num_of_turns = 2000 # track no. of turns, ex: 95500 for protons and 208151 for electrons
#////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////
#
# Application 6: [plot-eff-vs-time-proton.py & plot-eff-vs-time-electron.py] 
#                plot the efficiency vs. time
#
#////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////
#
# Application 7: [plot-phase-space-proton.py & plot-phase-space-electron.py]
#                plot the phase space for specific turn 
#
app7_num_of_turns = 100 # track no. of turns (95500 for protons) (208151 for electrons)
#////////////////////////////////////////////////////////////////////////////////////////////////////

