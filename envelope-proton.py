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

default_var_phi = 3.14 # set the initial phi 
default_var_dE = 0.0 # set the initial Delta_E
Delta_rad = 0.01 # rad = 3.1415 - (Delta_rad)*search_step

var_E = func.E_total_p(var_t)
var_beta2 = func.beta2_p(var_E)

var_dE = default_var_dE # need to varify in "while" loo
var_phi = default_var_phi # need to varify in "while" loop

show_dPoP = 9999.0*np.ones(num_of_turns)
show_phi = 9999.0*np.ones(num_of_turns)
search_step = 0 # start to search from 3.1415 to minus direction 

while (abs(show_phi[num_of_turns-1])>default_var_phi):
    for i in range(num_of_turns):
        var_dE, var_phi = func.iteration_p(var_dE, var_phi, var_t, var_E)
        show_phi[i] = var_phi
        show_dPoP[i] = var_dE/var_E/var_beta2
    search_step += 1
    var_phi = default_var_phi - Delta_rad*search_step 
    var_dE = default_var_dE
    print('start phi (Rad)= ', (var_phi + Delta_rad))

plt.figure(1)
##################################################
plt.xlim(para.set_xlim1, para.set_xlim2)
plt.ylim(para.set_ylim1, para.set_ylim2)
##################################################
plt.xlabel(r'$\phi$ (rad)', fontsize=20)
plt.ylabel(r'$\Delta P / P $ (%)', fontsize=20)
plt.plot(show_phi, 100.0*show_dPoP, 'b-', markeredgecolor = 'none', linewidth=4)
plt.grid(True)
plt.show()

