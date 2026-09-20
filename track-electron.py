#!/usr/bin/env python
from math import *
import numpy as np
import matplotlib.pyplot as plt
import BasicFunc as func
import Input as para

#################################################################################
num_of_turns = para.app3_num_of_turns # total number of turns for a ramping cycle
#################################################################################

default_var_phi = 3.14*2
default_var_dE = 0.0
var_phi = default_var_phi # need to varify in "while" loop
var_dE = default_var_dE # need to varify in "while" loop

var_t = 0.0 # set initial ramping time = 0 (s)  
var_E = func.E_total_e(var_t)

show_dPoP = 9999.0*np.ones(num_of_turns)
show_phi = 9999.0*np.ones(num_of_turns)
search_step = 0
Delta_rad = 0.01
# the bucket spans at most one RF period, so a search that sweeps
# more than 2*pi has nothing left to find
max_search_steps = int(2*pi/Delta_rad)

while (abs(show_phi[num_of_turns-1])>default_var_phi):
    if (search_step > max_search_steps):
        raise RuntimeError(
            'envelope search did not converge at t=%s s: no starting phase '
            'within 2*pi of %s rad stays inside the bucket. Check the RF '
            'settings (V_min, V_max, h) in Input.py.' % (var_t, default_var_phi))
    for i in range(num_of_turns):
        var_dE, var_phi = func.iteration_e(var_dE, var_phi, var_t, var_E)
        show_phi[i] = var_phi
        show_dPoP[i] = var_dE/var_E
        var_t = func.t_e_new(var_t, var_E)
        var_E = func.E_total_e(var_t)
    search_step += 1
    var_phi = default_var_phi - Delta_rad*search_step 
    var_dE = 0.0    
    print('start phi (Rad)= ', (var_phi + Delta_rad))

plt.figure(1)
##################################################
plt.xlim(para.set_xlim1, para.set_xlim2)
plt.ylim(para.set_ylim1, para.set_ylim2)
##################################################
plt.xlabel(r'$\phi$ (rad)', fontsize=20)
plt.ylabel(r'$\Delta E / E $ (%)', fontsize=20)
plt.plot(show_phi, 100.0*show_dPoP, 'ro-', markeredgecolor = 'none')
plt.grid(True)
plt.show()

