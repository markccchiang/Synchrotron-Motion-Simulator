#!/usr/bin/env python
from math import *
import numpy as np
import matplotlib.pyplot as plt
import _srcpath # noqa: F401 - puts ../src on sys.path
import BasicFunc as func

var_turn = 0 # initial number of turn = 0 turn
var_turn_reach_V_max = 0 # initial number of turn = 0 turn
var_t = 0 # initial time = 0 (s)
var_KE = func.KE(var_t) # initial kinetic energy (at t = 0)

MAX_element = 1000000 # maximum number of point to show in the plot
show_t = np.ones(MAX_element)
show_KE = np.ones(MAX_element)
show_V = np.ones(MAX_element)
show_phis = np.ones(MAX_element)
show_Q_s = np.ones(MAX_element)
show_alpha = np.ones(MAX_element)
show_area = np.ones(MAX_element)
show_v = np.ones(MAX_element)

while (var_KE<=(func.E_max-0.001)):

    if (var_turn >= MAX_element):
        raise RuntimeError(
            'plot-proton: the ramp needs more than %s turns; raise MAX_element.'
            % MAX_element)

    var_E = func.E_total_p(var_t)
    var_V = func.V_RF(var_t)
    var_KE = func.KE(var_t)
    var_phis = func.phis_p(var_t, var_E)
    var_Q_s = func.Q_s_p(var_E, var_V, var_t)
    var_alpha = func.alpha_ad_p(var_E, var_V, var_t)
    var_area = func.area_p(var_E, var_V, var_t)
    var_v = func.v_p(var_E)

    show_t[var_turn] = var_t
    show_KE[var_turn] = var_KE
    show_V[var_turn] = var_V
    show_phis[var_turn] = var_phis
    show_Q_s[var_turn] = var_Q_s
    show_alpha[var_turn] = var_alpha
    show_area[var_turn] = var_area
    show_v[var_turn] = var_v

    var_t = func.t_p_new(var_t, var_E)
    var_turn += 1

    if (var_V <= (func.V_max-0.001)):
        var_turn_reach_V_max += 1
    
print('total no. of turns: ', var_turn)
print('total no. of turns reaching maximunm RF voltage: ', var_turn_reach_V_max)
print('total ramping time (s): ', var_t)

plt.figure(1)
plt.xlabel('Time (ms)', fontsize=30)
plt.ylabel('Kinetic Energy (MeV)', fontsize=30)
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.plot(show_t[:var_turn]*1.0e+3, show_KE[:var_turn]*1.0e-6, 'b-', markeredgecolor = 'none', linewidth=4)
#plt.grid(True)
plt.savefig('proton_KE.eps', format='eps', dpi=1000, bbox_inches='tight')

plt.figure(2)
plt.xlabel('Time (ms)', fontsize=30)
plt.ylabel('RF Voltage (kV)', fontsize=30)
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.plot(show_t[:var_turn_reach_V_max]*1.0e+3, show_V[:var_turn_reach_V_max]*1.0e-3, 'b-', markeredgecolor = 'none', linewidth=4)
#plt.grid(True)
plt.savefig('proton_V_RF.eps', format='eps', dpi=1000, bbox_inches='tight')

plt.figure(3)
plt.xlabel('Time (ms)', fontsize=30)
plt.ylabel(r'$\phi_s$ (degree)', fontsize=30)
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.plot(show_t[:var_turn]*1.0e+3, show_phis[:var_turn]*180.0/3.1415926, 'b-', markeredgecolor = 'none', linewidth=4)
#plt.grid(True)
plt.savefig('proton_phis.eps', format='eps', dpi=1000, bbox_inches='tight')

plt.figure(4)
plt.xlabel('Time (ms)', fontsize=30)
plt.ylabel('Synchrotron Tune ($Q_s$)', fontsize=30)
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.plot(show_t[:var_turn]*1.0e+3, show_Q_s[:var_turn], 'b-', markeredgecolor = 'none', linewidth=4)
#plt.grid(True)
plt.savefig('proton_Qs.eps', format='eps', dpi=1000, bbox_inches='tight')

plt.figure(5)
plt.xlabel('Time (ms)', fontsize=30)
plt.ylabel('Adiabatic Coefficient (x$10^{-6}$)', fontsize=25)
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
#plt.plot(show_t[:var_turn]*1.0e+3, show_alpha[:var_turn]*1.0e+3, 'b-', markeredgecolor = 'none', linewidth=4)
plt.plot(show_t[:var_turn_reach_V_max]*1.0e+3, show_alpha[:var_turn_reach_V_max]*1.0e+6, 'b-', markeredgecolor = 'none', linewidth=4)
#plt.grid(True)
plt.savefig('proton_alpha_ad.eps', format='eps', dpi=1000, bbox_inches='tight')

plt.figure(6)
plt.xlabel('Time (ms)', fontsize=30)
plt.ylabel('Bucket Area', fontsize=30)
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.plot(show_t[:var_turn]*1.0e+3, show_area[:var_turn], 'b-', markeredgecolor = 'none', linewidth=4)
#plt.grid(True)
plt.savefig('proton_BArea.eps', format='eps', dpi=1000, bbox_inches='tight')

plt.figure(7)
plt.xlabel('Time (ms)', fontsize=30)
plt.ylabel('Particle Velocity (c)', fontsize=30)
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.plot(show_t[:var_turn]*1.0e+3, show_v[:var_turn]/func.c_speed, 'b-', markeredgecolor = 'none', linewidth=4)
#plt.grid(True)
#plt.text(0,0, r'an equation: $E=mc^2$', fontsize=15)
plt.savefig('proton_velocity.eps', format='eps', dpi=1000, bbox_inches='tight')

plt.show()

