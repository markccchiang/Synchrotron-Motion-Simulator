from math import *
import numpy as np
import Input as para

#
# input the booster ramping scenario 
#
E_min = para.E_min
E_max = para.E_max
f = para.f
L = para.L
alpha_c = para.alpha_c
rho = para.rho

#
# input the RF ramping settings
#
V_min = para.V_min
V_max = para.V_max
T_nu = para.T_nu
h = para.h

#
# physical parameters
#
PI = np.pi
c_speed = 299792458.0 # speed of light (m/s)
e_mass = 9.10938188e-31 # electron mass (kg)
p_mass = 1.67262158e-27 # proton mass(kg)
e_charge = 1.602176565e-19 # an electron charge (Columb)
C_gamma_e = 8.846e-32 # electron radiation coefficient: 
                      # 8.846e-5[m/(GeV)^3]=8.846e-5[m/(10^9eV)^3]=8.846e-32[m/(eV)^3]
C_gamma_p = 7.783e-45 # proton radiation coefficient:
                      # 7.783e-18[m/(GeV)^3]=7.783e-18[m/(10^9eV)^3]=7.783e-45[m/(eV)^3]

#
# note1: E is the total energy (mc^2 + kinetic energy)
# note2: t is time in the unit of (second)
#

def KE(t):
    if (E_max > E_min):
        DE = E_max-E_min
        alpha = (E_max+E_min)/(E_max-E_min)
        return (DE/2)*(alpha-cos(2*PI*f*t))
    else:
        return E_max

def E_total_p(t):
    return p_mass*c_speed**2 + e_charge*KE(t)

def E_total_e(t):
    return e_mass*c_speed**2 + e_charge*KE(t)

def V_RF(t):
    if ((0<t<T_nu) and (T_nu>0.0)):
        return (3*(t/T_nu)**2-2*(t/T_nu)**3)*(V_max-V_min)+V_min
    elif (t<=0):
        return V_min
    elif (t>=T_nu):
        return V_max
    else:
        raise ValueError('V_RF: t is not a valid number (got %s)' % t)

def gamma_e(E): 
    return E/(e_mass*c_speed**2)

def gamma_p(E):
    return E/(p_mass*c_speed**2)

def beta2_e(E):
    for_beta2_e = 1-(1/(gamma_e(E)**2))
    if (for_beta2_e >= 0):
        return for_beta2_e
    else:
        raise ValueError('beta2_e: beta^2 is negative (E=%s)' % E)

def beta2_p(E):
    for_beta2_p = 1-(1/(gamma_p(E)**2))
    if (for_beta2_p >= 0):
        return for_beta2_p
    else:
        raise ValueError('beta2_p: beta^2 is negative (E=%s)' % E)

def eta_e(E):
    return alpha_c-(1/(gamma_e(E)**2))

def eta_p(E):
    return alpha_c-(1/(gamma_p(E)**2))

def nu_s_e(E, V):
    return sqrt((h*abs(eta_e(E))*V*e_charge)/(2*PI*beta2_e(E)*E))

def nu_s_p(E, V):
    return sqrt((h*abs(eta_p(E))*V*e_charge)/(2*PI*beta2_p(E)*E))

def v_p(E):
    return sqrt(beta2_p(E))*c_speed

def v_e(E):
    return sqrt(beta2_e(E))*c_speed

def period_p(E):
    return L/v_p(E)

def period_e(E):
    return L/v_e(E)

def t_p_new(t, E):
    for_t_p_new = t + period_p(E)
    if (for_t_p_new >= 0):
        return for_t_p_new 
    else:
        return 0

def t_e_new(t, E):
    for_t_e_new = t + period_e(E)
    if (for_t_e_new >= 0):
        return for_t_e_new
    else:
        return 0

def t_p_old(t, E):
    for_t_p_old = t - period_p(E)
    if (for_t_p_old >= 0):
        return for_t_p_old
    else:
        return 0

def t_e_old(t, E):
    for_t_e_old = t - period_e(E)
    if (for_t_e_old >= 0):
        return for_t_e_old
    else:
        return 0

def U0_p(E):
    # Energy radiated per turn by a proton of total energy E, in joules.
    # C_gamma_p is quoted in m/eV^3, so the energy has to be expressed in eV
    # here; E is carried in joules everywhere else.
    return e_charge*C_gamma_p*((E/e_charge)**4)/rho

def U0_e(E):
    # Energy radiated per turn by an electron of total energy E, in joules.
    return e_charge*C_gamma_e*((E/e_charge)**4)/rho

def phis_p(t, E):
    KE_1 = KE(t_p_new(t, E))
    KE_0 = KE(t)
    if (KE_1>KE_0):
        gain = KE_1 - KE_0
    else:
        gain = 0.0
    # the synchronous particle must supply the ramp gain AND the energy it
    # radiates each turn; U0 is in joules, gain and V_RF are in eV/volts
    for_angle_p = (gain + U0_p(E)/e_charge)/V_RF(t)
    for_angle_p = max(-0.9999, min(0.9999, for_angle_p))
    return asin(for_angle_p) # (rad)

def phis_e(t, E):
    KE_1 = KE(t_e_new(t, E))
    KE_0 = KE(t)
    if (KE_1>KE_0):
        gain = KE_1 - KE_0
    else:
        gain = 0.0
    # the synchronous particle must supply the ramp gain AND the energy it
    # radiates each turn; U0 is in joules, gain and V_RF are in eV/volts
    for_angle_e = (gain + U0_e(E)/e_charge)/V_RF(t)
    for_angle_e = max(-0.9999, min(0.9999, for_angle_e))
    return asin(for_angle_e) # (rad)

def Q_s_p(E, V, t):
    return nu_s_p(E, V)*sqrt(abs(cos(phis_p(t, E))))

def Q_s_e(E, V, t):
    return nu_s_e(E, V)*sqrt(abs(cos(phis_e(t, E))))

def T_s_p(E, V, t):
    return period_p(E)/Q_s_p(E, V, t)

def T_s_e(E, V, t):
    return period_e(E)/Q_s_e(E, V, t)

def alpha_ad_p(E, V, t):
    return abs((T_s_p(E, V, t)-T_s_p(E, V, t_p_old(t, E)))/period_p(E))/(2*PI)

def alpha_ad_e(E, V, t):
    return abs((T_s_e(E, V, t)-T_s_e(E, V, t_e_old(t, E)))/period_e(E))/(2*PI)

def area_p(E, V, t):
    area_p_comp1 = 16*nu_s_p(E, V)/h/abs(eta_p(E))
    area_p_comp2 = (1-sin(phis_p(t, E)))/(1+sin(phis_p(t, E)))
    return area_p_comp1*area_p_comp2

def area_e(E, V, t):
    area_e_comp1 = 16*nu_s_e(E, V)/h/abs(eta_e(E))
    area_e_comp2 = (1-sin(phis_e(t, E)))/(1+sin(phis_e(t, E)))
    return area_e_comp1*area_e_comp2

def iteration_p(delta_E, phi, t, E):
    # phis_p already balances the synchronous particle's own radiation loss, so
    # what acts on the deviation is the excess this particle radiates over the
    # synchronous one. That difference is what damps the oscillation.
    E_radiation = U0_p(E + delta_E) - U0_p(E)
    delta_E_new = delta_E + e_charge*V_RF(t)*(sin(phi)-sin(phis_p(t, E)))-E_radiation
    phi_new = phi + 2*PI*h*eta_p(E)*delta_E_new/beta2_p(E)/E
    return delta_E_new, phi_new

def iteration_e(delta_E, phi, t, E):
    # see iteration_p: the synchronous loss is carried by phis_e, so only the
    # excess over it acts on the deviation
    E_radiation = U0_e(E + delta_E) - U0_e(E)
    delta_E_new = delta_E + e_charge*V_RF(t)*(sin(phi)-sin(phis_e(t, E)))-E_radiation
    phi_new = phi + 2*PI*h*eta_e(E)*delta_E_new/beta2_e(E)/E
    return delta_E_new, phi_new

