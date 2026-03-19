#!/usr/bin/env python
from math import *
import numpy as np
import BasicFunc as func
import Input as para

###########################################################################################
num_of_particles = para.num_of_particles # set no. of particles of a beam for tracking
num_of_turns = para.app5_num_of_turns+1 # track no. of turns 
sigma_dPoP = para.sigma_dPoP # set the sigma of (+/-) Delta_E/E
mean_dPoP = para.mean_dPoP # set the mean of (+/-) Delta_E/E
range_dPoP = para.range_dPoP # define the survival range of Delta_E/E
range_phi1 = para.range_phi1 # define the lower limit of survival range phi (rad) for protons
range_phi2 = para.range_phi2 # define the upper limit of survival range phi (rad) for protons
###########################################################################################

var_t_tmp = 0.0 # set initial ramping time = 0 (s)
var_t = np.zeros(num_of_particles) # start ramping from t=0 (sec) 
var_E = func.E_total_e(var_t_tmp)*np.ones(num_of_particles)

var_E_tmp = func.E_total_e(var_t_tmp)
var_beta2_tmp = func.beta2_e(var_E_tmp)
var_beta2 = func.beta2_e(var_E_tmp)*np.ones(num_of_particles)

# assume the dE distribution is the gaussian with the mean and sigma
np.random.seed(12345)
var_dE = mean_dPoP + sigma_dPoP*np.random.randn(num_of_particles)*var_E_tmp

# assume the phi is randomly distributed between [0, +2pi]
np.random.seed(34567) 
var_phi = np.pi*2.0*np.random.random(num_of_particles)

show_phi = np.zeros(num_of_particles) 
show_dPoP = np.zeros(num_of_particles) 
show_eff = 9999.0*np.ones(num_of_turns)
show_turn = 9999*np.ones(num_of_turns)
show_time = 9999*np.ones(num_of_turns)

for i in range(num_of_turns):
    count = 0
    eff = 0.0
    for j in range(num_of_particles):

        show_phi[j] = var_phi[j]
        show_dPoP[j] = var_dE[j]/var_E[j]

        var_dE[j], var_phi[j] = func.iteration_e(var_dE[j], var_phi[j], var_t[j], var_E[j])

        var_t[j]  = func.t_e_new(var_t[j], var_E[j])
        time_tmp = var_t[j]

        var_E[j] = func.E_total_e(var_t[j])
        var_beta2[j] = func.beta2_e(var_E[j])

        if (range_phi1<=show_phi[j]<=range_phi2 and abs(show_dPoP[j])<=range_dPoP):
        #if (abs(show_dPoP[j])<=range_dPoP):
            count +=1

    eff = 100.0*count/num_of_particles
    show_eff[i] = eff
    show_turn[i] = i
    show_time[i] = time_tmp*1000
    #print 'turn= ', i, ' ; capture rate (%)= ', eff

print(para.V_min, ' ', para.T_nu, ' ', para.sigma_dPoP, ' ', eff)
#np.savetxt('eff-electron.dat', (show_turn, show_eff), fmt='%3.2f')
np.savetxt('eff-electron.dat', (show_time, show_eff), fmt='%3.4f')

