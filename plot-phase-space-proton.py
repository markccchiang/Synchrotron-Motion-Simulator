#!/usr/bin/env python
from math import *
import numpy as np
import matplotlib.pyplot as plt
import BasicFunc as func
import Input as para

###########################################################################################
num_of_turns = para.app7_num_of_turns+1 # set track no. of turns for plotting
num_of_particles = para.num_of_particles # set no. of particles of a beam for tracking
###########################################################################################
sigma_dPoP = para.sigma_dPoP # set the sigma of (+/-) Delta_P/P
mean_dPoP = para.mean_dPoP # set the mean of (+/-) Delta_P/P
range_dPoP = para.range_dPoP # define the survival range of Delta_P/P
range_phi1 = para.range_phi1 # define the lower limit of survival range phi (rad) for protons
range_phi2 = para.range_phi2 # define the upper limit of survival range phi (rad) for protons
###########################################################################################

var_t_tmp = 0.0 # set initial ramping time = 0 (s)
var_t = var_t_tmp # every particle shares one machine clock
var_E = func.E_total_p(var_t_tmp)

var_E_tmp = func.E_total_p(var_t_tmp)
var_beta2_tmp = func.beta2_p(var_E_tmp)
var_beta2 = func.beta2_p(var_E_tmp)

# assume the dE distribution is the gaussian with the mean and sigma
np.random.seed(12345)
var_dE = mean_dPoP + sigma_dPoP*np.random.randn(num_of_particles)*var_E_tmp*var_beta2_tmp

# assume the phi is randomly distributed between [-pi, +pi]
np.random.seed(34567) 
var_phi = np.pi*2.0*np.random.random(num_of_particles)-np.pi

show_phi = np.zeros(num_of_particles) 
show_dPoP = np.zeros(num_of_particles) 
show_eff = 9999.0*np.ones(num_of_turns)
show_turn = 9999*np.ones(num_of_turns)

#
# Track particles
#
for i in range(num_of_turns):
    count = 0
    eff = 0.0
    time = 0.0
    for j in range(num_of_particles):

        show_phi[j] = var_phi[j]
        show_dPoP[j] = var_dE[j]/var_E/var_beta2

        var_dE[j], var_phi[j] = func.iteration_p(var_dE[j], var_phi[j], var_t, var_E)

        if (range_phi1<=show_phi[j]<=range_phi2 and abs(show_dPoP[j])<=range_dPoP):
            count +=1

    # t, E and beta^2 are the same for every particle, so advance them once
    var_t = func.t_p_new(var_t, var_E)
    time_tmp = var_t
    var_E = func.E_total_p(var_t)
    var_beta2 = func.beta2_p(var_E)

    eff = 100.0*count/num_of_particles
    time = time_tmp
    show_eff[i] = eff
    show_turn[i] = i
    print('turn= ', i, ' time (ms)= ', 1000*time, ' ; capture rate (%)= ', eff)

#
# define the envelop function
#
def envelop(set_t):

    var_t = set_t # (sec) set the ramping time point to get the envelope 
    var_E = func.E_total_p(var_t) # the initial total energy
    var_beta2 = func.beta2_p(var_E) # the initial beta^2
    default_var_phi = 3.14 # set the initial phi (rad)
    default_var_dE = 0.0 # set the initial Delta_E
    var_phi = default_var_phi # need to varify in "while" loop
    var_dE = default_var_dE # need to varify in "while" loop
    ##########################################################################
    num_of_turns = 3000 # number of turns for plotting envelope
    ##########################################################################
    show_dPoP = 9999.0*np.ones(num_of_turns)
    show_phi = 9999.0*np.ones(num_of_turns)
    search_step = 0 # start fo search from 3.1415 to minus direction 
    Delta_rad = 0.01 # rad = 3.1415 - Delta_rad*search_step
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
            var_dE, var_phi = func.iteration_p(var_dE, var_phi, var_t, var_E)
            show_phi[i] = var_phi
            show_dPoP[i] = var_dE/var_E/var_beta2
        search_step += 1
        var_phi = default_var_phi - Delta_rad*search_step 
        var_dE = default_var_dE
    return show_phi, show_dPoP

#
# create the envelop lines
#
envelop_phi, envelop_dPoP = envelop(time)

plt.figure(1)
plt.xlim(para.set_xlim1, para.set_xlim2)
plt.ylim(para.set_ylim1, para.set_ylim2)
plt.xlabel(r'$\phi$ (rad)', fontsize=30)
plt.ylabel(r'$\Delta P / P $ (%)', fontsize=30)
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.title('$%3.2f$ ms; capture rate: $%3.1f$%%' %(time*1000, eff), fontsize=30)
plt.plot(show_phi, 100.0*show_dPoP, 'ro', markeredgecolor = 'none')
plt.plot(envelop_phi, 100.0*envelop_dPoP, 'k-', markeredgecolor = 'none', linewidth=2)
#plt.grid(True)
plt.savefig('proton_phase_space.eps', format='eps', dpi=1000, bbox_inches='tight')

plt.show()

