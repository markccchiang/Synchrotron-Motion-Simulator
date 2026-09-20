#!/usr/bin/env python
from math import *
import numpy as np
import matplotlib.pyplot as plt
import BasicFunc as func
import Input as para

############################################################################
var_t = para.app1_set_t # (s) set the ramping time point to get the envelope 
num_of_turns = para.app1_num_of_turns # set the number of turns for tracking
############################################################################

show_phi, show_dPoP = func.envelope_e(var_t, num_of_turns)

plt.figure(1)
##################################################
plt.xlim(para.set_xlim1, para.set_xlim2)
plt.ylim(para.set_ylim1, para.set_ylim2)
##################################################
plt.xlabel(r'$\phi$ (rad)', fontsize=20)
plt.ylabel(r'$\Delta E / E $ (%)', fontsize=20)
plt.plot(show_phi, 100.0*show_dPoP, 'b-', markeredgecolor = 'none', linewidth=4)
plt.grid(True)
plt.show()

