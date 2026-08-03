def compute_gain_xy(vcm, vref, vout):
    """
    Solves for x and y from two equations:
      vo1 - vref1 = x*(v11 + vref1) + y*(v11 + vo1)
      vo2 - vref2 = x*(v12 + vref2) + y*(v12 + vo2)
    
    Parameters:
        vo1, vref1, v11 : values from first equation
        vo2, vref2, v12 : values from second equation
    
    Returns:
        x, y : solution to the system
    """
    Vcm=vcm
    Vout=vout
    Vref=vref
    A1 = Vcm[0] + Vref[0]
    B1 = Vcm[0] + Vout[0]
    C1 = Vout[0] - Vref[0]

    A2 = Vcm[0] + Vref[1]
    B2 = Vcm[0] + Vout[1]
    C2 = Vout[0] - Vref[1]

    denominator = A1 * B2 - A2 * B1

    if denominator == 0:
        raise ValueError("Denominator is zero, can't solve the system (singular matrix)")

    x = (C1 * B2 - C2 * B1) / denominator
    y = (A1 * C2 - A2 * C1) / denominator

    return x, y


x,y = compute_gain_xy((2.5-1.300730,2.5-2.30065), (2.5,2.5), (2.5+0.036455100, 2.5+0.0535932))
print(f"x = {x}, y = {y}")