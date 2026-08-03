from constants import G0
from math import log10

def gain_error_differential(V21, VO1, V22, VO2):

    G1 = G0 + (VO2-VO1)/(V22-V21)

    return G1

def gain_error_standard(V21, VO1, V22, VO2):

    G1 = (VO2-VO1)/(V22-V21)

    return G1

def cmrr_standard(VCM1, VO1, VCM2, VO2, Gain, V21, V22):

    Vsense_diff = V22 - V21
    VO_diff = VO2 - VO1 - Vsense_diff*Gain
    VCM_diff = VCM2 - VCM1
    
    CM_gain = (VO_diff)/(VCM_diff)

    xy_diff = CM_gain*(Gain+1)
    
    return xy_diff

def CMRR_error_differential(VCM1, VO1, VCM2, VO2, x, V21, V22):

    Vsense_diff = V22 - V21
    VO_diff = VO2 - VO1 - Vsense_diff*x
    VCM_diff = VCM2 - VCM1
    

    error = ((VO_diff)*(x+1))/(VCM_diff - VO_diff)

    return error

def CMRR_calc(error):
    abs_error = abs(error)
    CMRR = 20*log10((G0+1)/abs_error) + 20*log10(G0)

    return CMRR

