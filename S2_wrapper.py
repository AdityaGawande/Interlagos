import instr_control
import instr_math
import instr_dummy
from constants import G0 as Gain_ideal

def gain_error_measurement_init():
    # Set VREF to 2.5V - SMUchA
    instr_dummy.SMUchA_voltage_set(2.5)
    # Set VCM to 0.5V - SMU_bad
    instr_dummy.SMUbad_voltage_set(0.5)

def cmrr_measurement_init():
    # Set VREF to 2.5V - SMUchA
    instr_dummy.SMUchA_voltage_set(2.5)
    # Set Isense = 5mA - SMUchB
    instr_dummy.SMUchB_current_set(0)
    
def cmrr_measurement_single(Gain_ideal):
    # Set VCM to 0.5V - SMU_bad
    instr_dummy.SMUbad_voltage_set(0.5)
    
    # Measure Vsense(V21) and Vout(VO1) at the same time
    V21, VO1, VCM1 = instr_control.dmm_measure_x3()

    # Set VCM to 0.5V - SMU_bad
    instr_dummy.SMUbad_voltage_set(8)
    # Measure Vsense(V22) and Vout(VO2) at the same time
    V22, VO2, VCM2 = instr_control.dmm_measure_x3()

    xy_diff = instr_math.cmrr_standard(VCM1, VO1, VCM2, VO2, Gain_ideal, V21, V22)
    print(xy_diff, V22-V21, V21, V22, VO2-VO1, VO1, VO2, VCM2-VCM1, VCM1, VCM2)
    
def gain_error_measurement_single(Gain_ideal):
    # Set Isense = 5mA - SMUchB
    instr_dummy.SMUchB_current_set(5e-3)
    # Set VCM to 0.5V - SMU_bad
    instr_dummy.SMUbad_voltage_set(0.5)

    # Measure Vsense(V21) and Vout(VO1) at the same time
    V21, VO1, VCM1 = instr_control.dmm_measure_x3()

    # Set Isense = -5mA - SMUchB
    instr_dummy.SMUchB_current_set(-5e-3)
    # Measure Vsense(V22) and Vout(VO2) at the same time
    V22, VO2, VCM2 = instr_control.dmm_measure_x3()

    G1 = instr_math.gain_error_standard(V21, VO1, V22, VO2)
    
    print(G1-Gain_ideal, G1, V22-V21, V21, V22, VO2-VO1, VO1, VO2, VCM2-VCM1, VCM1, VCM2)

def cmrr_measurement(n, Gain_ideal, PLC):
    print(f"Measuring xy_diff using the standard method at PLC of {PLC}")
    print()
    
    cmrr_measurement_init()
    
    print("XY_DIFF, VDIFF, VDIFF1, VDIFF2, VOUT, VOUT1, VOUT2, VCM, VCM1, VCM2")
    for i in range(0, n):
        cmrr_measurement_single(Gain_ideal)

def gain_error_measurement(n, Gain_ideal, PLC):
    print(f"Measuring Gain using the standard method at PLC of {PLC}")
    print()
    
    gain_error_measurement_init()
    
    print("Gain Error, Gain, VDIFF, VDIFF1, VDIFF2, VOUT, VOUT1, VOUT2, VCM, VCM1, VCM2")
    for i in range(0, n):
        gain_error_measurement_single(Gain_ideal)
        
    # gain_error_measurement_exit() # Turn off output from SMUs
        

from datetime import datetime
now = str(datetime.now())
print("Test started at", now)
print()

length = 10
# Gain_ideal = 50

# PLC = 1
# gain_error_measurement(length, Gain_ideal, PLC)
# print()

# PLC = 10
# gain_error_measurement(length, Gain_ideal, PLC)
# print()

PLC = 100
cmrr_measurement(length, Gain_ideal, PLC)
print()
