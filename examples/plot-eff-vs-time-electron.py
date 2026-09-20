#!/usr/bin/env python
from math import *
import numpy as np
import matplotlib.pyplot as plt
import _srcpath # noqa: F401 - puts ../src on sys.path
import Input as para

#data = np.loadtxt("eff-proton.dat")
data = np.loadtxt("eff-electron.dat")

show_time = data[0]
show_eff = data[1]
#print show_turn, show_eff

#x_lower_limit = min(show_time)
#x_upper_limit = max(show_time)
x_lower_limit = 0.0
x_upper_limit = para.T_nu*1000

y_lower_limit = min(show_eff)-abs(max(show_eff)-min(show_eff))
y_upper_limit = max(show_eff)

plt.figure()
plt.xlabel('Time (ms)', fontsize=30)
plt.ylabel('Capture rate (%)', fontsize=30)
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.xlim(x_lower_limit, x_upper_limit)
plt.ylim(y_lower_limit, y_upper_limit)
plt.plot(show_time, show_eff, 'b-', markeredgecolor = 'b', linewidth=5)

#plt.savefig('eff-vs-time-proton.eps', format='eps', dpi=1000, bbox_inches='tight')
plt.savefig('eff-vs-time-electron.eps', format='eps', dpi=1000, bbox_inches='tight')

plt.show()

