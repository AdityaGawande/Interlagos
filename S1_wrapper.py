import instr_control
import instr_math
from constants import G0 as Gain_ideal

def gain_error_measurement_init():

    # Set VREF to 2.5V - SMUchA
    # instr_control.SMUchA_voltage_set(2.5)
    # Set VCM to 0.5V - SMU_bad
    instr_control.SMUbad_voltage_set(0.5) 

def gain_error_measurement_single(Gain_ideal, dmm1, dmm2, dmm3):
    # Set Isense = 5mA - SMUchB
        instr_control.SMUchB_current_set(5e-5)
        # Measure Vsense(V21) and Vout(VO1) at the same time
        V21, VO1, VCM1 = instr_control.dmm_measure_x3_single(dmm1, dmm2, dmm3)
    
        # Set Isense = -5mA - SMUchB
        instr_control.SMUchB_current_set(-5e-5)
        # Measure Vsense(V22) and Vout(VO2) at the same time
        V22, VO2, VCM2 = instr_control.dmm_measure_x3_single(dmm1, dmm2, dmm3)
    
        G1 = instr_math.gain_error_standard(V21, VO1, V22, VO2)
        
        print(G1-Gain_ideal, G1, V22-V21, V21, V22, VO2-VO1, VO1, VO2, VCM2-VCM1, VCM1, VCM2)

def gain_error_measurement(n, Gain_ideal, PLC):
    print(f"Measuring Gain using the standard method at PLC of {PLC}")
    print()
    
    gain_error_measurement_init()
    dmm1, dmm2, dmm3 = instr_control.dmm_measure_x3_setup()
    
    print("Gain Error, Gain, VDIFF, VDIFF1, VDIFF2, VOUT, VOUT1, VOUT2, VCM, VCM1, VCM2")
    for i in range(0, n):
        gain_error_measurement_single(Gain_ideal, dmm1, dmm2, dmm3)

    instr_control.dmm_measure_x3_deinit(dmm1, dmm2, dmm3)

from datetime import datetime
now = str(datetime.now())
print("Test started at", now)
print()

length = 100
# Gain_ideal = 50

# PLC = 1
# gain_error_measurement(length, Gain_ideal, PLC)
# print()

# PLC = 10
# gain_error_measurement(length, Gain_ideal, PLC)
# print()

PLC = 100
gain_error_measurement(length, Gain_ideal, PLC)
print()
