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
# the envelope turn count lives with the other app2 settings below

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
plt.ylabel(r'$\Delta P / P $ (%)', fontsize=20)

#
# animation settings
#
#####################################################################################
set_start_t = para.app2_set_start_t # set the start time (s)
set_final_t = para.app2_set_final_t # set the final time (s)
num_of_turns = para.app2_num_of_turns # turns used to trace the envelope
num_of_intervals = para.app2_num_of_intervals # no. of plots to show in the animation
#####################################################################################

set_t = 0.0 # initialize the ramping time variable (s)
resolution = 100 # animation resolution

with writer.saving(fig, "envelope-animation-proton.mp4", resolution):
    for i in range(num_of_intervals+1):
        set_t = set_start_t + (set_final_t/(num_of_intervals))*i
        show_phi, show_dPoP = func.envelope_p(set_t, num_of_turns)
        print('ramping time (s)= ', set_t)
        l.set_data(show_phi, 100.0*show_dPoP)
        #ttl.set_text('$%3.4f$ s' %(set_t))
        ax.set_title('$%3.1f$ ms' %(set_t*1000), fontsize=30)
        writer.grab_frame()

