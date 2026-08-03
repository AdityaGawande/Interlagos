import numpy as np

def compute_x_y(vsen, vo, vcm):
    # Ensure input arrays are of length 3
    assert len(vsen) == len(vo) == len(vcm) == 3, "Arrays must all be of length 3"
   
    vsen1, vsen2, vsen3 = vsen
    vo1, vo2, vo3 = vo
    vcm1, vcm2, vcm3 = vcm
    xc=50
    error=0
    yc=xc+error

    # # Numerators
    # num_x = (
    #     vcm1*vo2 - vcm2*vo1 - vcm1*vo3 + vcm3*vo1 + vcm2*vo3 - vcm3*vo2 +
    #     50*vcm1*vsen2 - 50*vcm2*vsen1 - 50*vcm1*vsen3 + 50*vcm3*vsen1 +
    #     50*vcm2*vsen3 - 50*vcm3*vsen2 - vo1*vsen2 + vo2*vsen1 +
    #     vo1*vsen3 - vo3*vsen1 - vo2*vsen3 + vo3*vsen2
    # )

    # den_x = (
    #     vcm1*vsen2 - vcm2*vsen1 - vcm1*vsen3 + vcm3*vsen1 +
    #     vcm2*vsen3 - vcm3*vsen2
    # )

    # num_y = (
    #     vcm1*vo2 - vcm2*vo1 - vcm1*vo3 + vcm3*vo1 + vcm2*vo3 - vcm3*vo2 +
    #     50*vcm1*vsen2 - 50*vcm2*vsen1 - 50*vcm1*vsen3 + 50*vcm3*vsen1 +
    #     50*vcm2*vsen3 - 50*vcm3*vsen2
    # )

    # den_y = (
    #     vcm1*vsen2 - vcm2*vsen1 - vcm1*vsen3 + vcm3*vsen1 +
    #     vcm2*vsen3 - vcm3*vsen2 - vo1*vsen2 + vo2*vsen1 +
    #     vo1*vsen3 - vo3*vsen1 - vo2*vsen3 + vo3*vsen2
    # )
    x=(vcm1*vo2 - vcm2*vo1 - vcm1*vo3 + vcm3*vo1 + vcm2*vo3 - vcm3*vo2 - vo1*vsen2 + vo2*vsen1 + vo1*vsen3 - vo3*vsen1 - vo2*vsen3 + vo3*vsen2 + vcm1*vsen2*xc - vcm2*vsen1*xc - vcm1*vsen3*xc + vcm3*vsen1*xc + vcm2*vsen3*xc - vcm3*vsen2*xc)/(vcm1*vsen2 - vcm2*vsen1 - vcm1*vsen3 + vcm3*vsen1 + vcm2*vsen3 - vcm3*vsen2)


    y=(vcm1*vo2 - vcm2*vo1 - vcm1*vo3 + vcm3*vo1 + vcm2*vo3 - vcm3*vo2 + vcm1*vo2*yc - vcm2*vo1*yc - vcm1*vo3*yc + vcm3*vo1*yc + vcm2*vo3*yc - vcm3*vo2*yc + vcm1*vsen2*yc - vcm2*vsen1*yc - vcm1*vsen3*yc + vcm3*vsen1*yc + vcm2*vsen3*yc - vcm3*vsen2*yc + vcm1*vsen2*xc*yc - vcm2*vsen1*xc*yc - vcm1*vsen3*xc*yc + vcm3*vsen1*xc*yc + vcm2*vsen3*xc*yc - vcm3*vsen2*xc*yc)/(vcm1*vsen2 - vcm2*vsen1 - vcm1*vsen3 + vcm3*vsen1 + vcm2*vsen3 - vcm3*vsen2 - vo1*vsen2 + vo2*vsen1 + vo1*vsen3 - vo3*vsen1 - vo2*vsen3 + vo3*vsen2 + vcm1*vsen2*xc - vcm2*vsen1*xc - vcm1*vsen3*xc + vcm3*vsen1*xc + vcm2*vsen3*xc - vcm3*vsen2*xc - vo1*vsen2*yc + vo2*vsen1*yc + vo1*vsen3*yc - vo3*vsen1*yc - vo2*vsen3*yc + vo3*vsen2*yc)

    return x, y

