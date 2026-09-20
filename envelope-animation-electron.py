#!/usr/bin/env python
from math import *
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as manimation
import BasicFunc as func
import Input as para

#
# define the running functions
#
def run(set_t):

    var_t = set_t # (sec) set the ramping time point to get the envelope 
    var_E = func.E_total_e(var_t) # the initial total energy
    var_beta2 = func.beta2_e(var_E) # the initial beta^2
    default_var_phi = 3.14*2 # set the initial phi (rad)
    default_var_dE = 0.0 # set the initial Delta_E
    var_phi = default_var_phi # need to varify in "while" loop
    var_dE = default_var_dE # need to varify in "while" loop
    ##########################################################################
    num_of_turns = para.app2_num_of_turns # total number of turns for tracking
    ##########################################################################
    show_dPoP = 9999.0*np.ones(num_of_turns)
    show_phi = 9999.0*np.ones(num_of_turns)
    search_step = 0 # start fo search from 3.1415 to minus direction 
    Delta_rad = 0.001 # rad = 3.14*2 - Delta_rad*search_step

    while (abs(show_phi[num_of_turns-1])>default_var_phi):
        for i in range(num_of_turns):
            var_dE, var_phi = func.iteration_e(var_dE, var_phi, var_t, var_E)
            show_phi[i] = var_phi
            show_dPoP[i] = var_dE/var_E
        search_step += 1
        var_phi = default_var_phi - Delta_rad*search_step 
        var_dE = default_var_dE
    return show_phi, show_dPoP

#
# set the animation commands
#
FFMpegWriter = manimation.writers['ffmpeg']
metadata = dict(title='Movie Show', artist='Matplotlib', comment='Movie support!')
writer = FFMpegWriter(fps=20, metadata=metadata)

#
# set the animation plot forms
#
fig = plt.figure()
l, = plt.plot([], [], 'b-', markeredgecolor = 'none', linewidth=4)

#
# set the text position
#
ax = plt.axes()
#ttl = ax.text(0.4, 0.9, '', transform = ax.transAxes, va='center', fontsize=30)

#
# plot settings
#
##################################################
plt.xlim(para.set_xlim1, para.set_xlim2)
plt.ylim(para.set_ylim1, para.set_ylim2)
##################################################
plt.xlabel(r'$\phi$ (rad)', fontsize=20)
plt.ylabel(r'$\Delta E / E $ (%)', fontsize=20)

#
# animation settings
#
#####################################################################################
set_start_t = para.app2_set_start_t # set the start time (s)
set_final_t = para.app2_set_final_t # set the final time (s)
num_of_intervals = para.app2_num_of_intervals # no. of plots to show in the animation
#####################################################################################

set_t = 0.0 # initialize the ramping time variable (s)
resolution = 100 # animation resolution

with writer.saving(fig, "envelope-animation-electron.mp4", resolution):
    for i in range(num_of_intervals+1):
        set_t = set_start_t + (set_final_t/(num_of_intervals))*i
        show_phi, show_dPoP = run(set_t)
        print('ramping time (s)= ', set_t)
        l.set_data(show_phi, 100.0*show_dPoP)
        #ttl.set_text('$%3.4f$ s' %(set_t))
        ax.set_title('$%3.1f$ ms' %(set_t*1000), fontsize=30)
        writer.grab_frame()

