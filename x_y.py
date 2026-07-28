import numpy as np

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

