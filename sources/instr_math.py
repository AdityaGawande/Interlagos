from sources.constants import G0
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

def compute_x_y(vsen, vo, vcm):
    # Ensure input arrays are of length 3
    assert len(vsen) == len(vo) == len(vcm) == 3, "Arrays must all be of length 3"
   
    vsen1, vsen2, vsen3 = vsen
    vo1, vo2, vo3 = vo
    vcm1, vcm2, vcm3 = vcm

    # Numerators
    num_x = (
        vcm1*vo2 - vcm2*vo1 - vcm1*vo3 + vcm3*vo1 + vcm2*vo3 - vcm3*vo2 +
        50*vcm1*vsen2 - 50*vcm2*vsen1 - 50*vcm1*vsen3 + 50*vcm3*vsen1 +
        50*vcm2*vsen3 - 50*vcm3*vsen2 - vo1*vsen2 + vo2*vsen1 +
        vo1*vsen3 - vo3*vsen1 - vo2*vsen3 + vo3*vsen2
    )

    den_x = (
        vcm1*vsen2 - vcm2*vsen1 - vcm1*vsen3 + vcm3*vsen1 +
        vcm2*vsen3 - vcm3*vsen2
    )

    num_y = (
        vcm1*vo2 - vcm2*vo1 - vcm1*vo3 + vcm3*vo1 + vcm2*vo3 - vcm3*vo2 +
        50*vcm1*vsen2 - 50*vcm2*vsen1 - 50*vcm1*vsen3 + 50*vcm3*vsen1 +
        50*vcm2*vsen3 - 50*vcm3*vsen2
    )

    den_y = (
        vcm1*vsen2 - vcm2*vsen1 - vcm1*vsen3 + vcm3*vsen1 +
        vcm2*vsen3 - vcm3*vsen2 - vo1*vsen2 + vo2*vsen1 +
        vo1*vsen3 - vo3*vsen1 - vo2*vsen3 + vo3*vsen2
    )

    x = num_x / den_x
    y = num_y / den_y

    return x, y
