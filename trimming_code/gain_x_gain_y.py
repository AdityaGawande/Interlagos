
# --- Function Definition ---
def compute_gain_xy(vcm, vsense, vout):
    V1_array = vcm
    V2_array = vsense*0.9967534557
    VO1_array = vout
    

    # First measurement set
    V11 = V1_array[0] 
    V21 = V1_array[0] + V2_array[0] 
    VO11 = VO1_array[0]

    # Second measurement set
    V12 = V1_array[1] 
    V22 = V1_array[1] + V2_array[1]
    VO21 = VO1_array[1] 

    # Third measurement set
    V13 = V1_array[2] 
    V23 = V1_array[2] + V2_array[2]
    VO31 = VO1_array[2] 

    # Gain X
    numerator_x = V21 * VO21 - V22 * VO11 - V21 * VO31 + V23 * VO11 + V22 * VO31 - V23 * VO21
    denominator_x = V11 * V22 - V12 * V21 - V11 * V23 + V13 * V21 + V12 * V23 - V13 * V22
    gainx = numerator_x / denominator_x

    # Gain Y
    numerator_y = V11 * VO21 - V12 * VO11 - V11 * VO31 + V13 * VO11 + V12 * VO31 - V13 * VO21
    denominator_y = denominator_x + (
        - V11 * VO21 + V12 * VO11 + V11 * VO31 - V13 * VO11 - V12 * VO31 + V13 * VO21 +
        V21 * VO21 - V22 * VO11 - V21 * VO31 + V23 * VO11 + V22 * VO31 - V23 * VO21
    )
    gainy = numerator_y / denominator_y

    return gainx, gainy

