import instr_control
import instr_combined
import instr_math
import time
from math import log10

def gain_error_measurement_init():

    # Set VREF to 2.5V - SMUchA
    instr_control.SMUchA_voltage_set(2.5)
    # Set VCM to 0.5V - SMU_bad
    instr_control.SMUbad_voltage_set(0.5)


def gain_error_measurement_single():
    
    # Set Isense = 5mA - SMUchB
    instr_control.SMUchB_current_set(5e-3)
    # Measure Vsense(V21) and Vout(VO1) at the same time
    V21, VO1, VCM = instr_control.dmm_measure_x3()
    # print(V21, VO1, VCM)

    # Set Isense = -5mA - SMUchB
    instr_control.SMUchB_current_set(-5e-3)
    # Measure Vsense(V22) and Vout(VO2) at the same time
    V22, VO2, VCM = instr_control.dmm_measure_x3()
    # print(V22, VO2, VCM)
    # print(f"vsense1: {V21}, vsense2: {V22}")
    # print(f"vout1: {VO1}, vout2: {VO2}")


    G1 = instr_math.gain_error_differential(V21, VO1, V22, VO2)
    
    # G1=49.55124505455

    return G1

def CMRR_error_measurement_init():
    # Set VREF to 2.5V - SMUchA
    instr_control.SMUchA_voltage_set(2.5)
    # Set Isense to 0 - SMUchB
    instr_control.SMUchB_current_set(0)
    print("Connecting Vsense resistor")
    instr_control.vsense_res_connect()
    # x = float(input("Enter Gain value from previous readings - "))
    x = 50
    return x

# def CMRR_error_measurement_init():
#     x = input("Enter Gain value from previous readings -")
#     return x

def CMRR_error_measurement_single(x):

    # Set VCM to 0.5V - SMU_bad
    instr_control.SMUbad_voltage_set(0.5)
    # Measure VO1 and VCM1
    V21, VO1, VCM1 = instr_control.dmm_measure_x3()
    # print(V2, VO1, VCM1)

    # Set VCM to 8V
    instr_control.SMUbad_voltage_set(5)
    # Measure VO2 and VCM2
    V22, VO2, VCM2 = instr_control.dmm_measure_x3()
    # print(V2, VO2, VCM2)

    error = instr_math.CMRR_error_differential(VCM1, VO1, VCM2, VO2, x, V21, V22)
    # print(f"vcm1: {VCM1}, vcm2: {VCM2}")
    # print(f"vout1: {VO1}, vout2: {VO2}")
    # print(f"vsense1: {V21}, vsense2: {V22}")
    # error = 0.208454545458
    Vsense_diff = V22 - V21
    VO_diff = VO2 - VO1 - Vsense_diff*x
    voltage_error = (VO_diff)/(VCM2 - VCM1)

    CMRR = 20*log10(abs(1/voltage_error)) + 20*log10(50)

    # CMRR = 101.1158454

    return error, CMRR, voltage_error

def gain_cmrr_error_measurement_single():

    gainx, gainy = instr_combined.combined_measurement()

    yx_error = gainy - gainx
    CMRR = instr_math.CMRR_calc(yx_error)

    # gainx, gainy, yx_error, CMRR = 49.55124505455, 49.25124505455, -0.3484864, 102.485464456 

    return gainx, gainy, yx_error, CMRR

def honest_to_god_cmrr_init():
    # Set VREF to 2.5V - SMUchA
    instr_control.SMUchA_voltage_set(2.5)
    # Set Isense to 0 - SMUchB
    instr_control.SMUchB_current_set(0)
    # Connect Vsense resistor
    print("Connecting Vsense resistor")
    instr_control.vsense_res_connect()

def standard_gain_measure_init():
    # Set VREF to 2.5V - SMUchA
    instr_control.SMUchA_voltage_set(2.5)
    # # Set Isense to 0 - SMUchB - not required here
    # instr_control.SMUchB_current_set(0)
    # Connect Vsense resistor
    print("Connecting Vsense resistor")
    instr_control.vsense_res_connect()  # Change function so that it is not intrusive to the supplies on ch1 and ch2
    
    

def honest_to_god_cmrr_single():

    # Set VCM to 0.5V - SMU_bad
    instr_control.SMUbad_voltage_set(0.5)
    # Measure VO1 and VCM1
    V2, VO1, VCM1 = instr_control.dmm_measure_x3()
    # print(V2, VO1, VCM1)

    time.sleep(2)

    # Set VCM to 8V - SMU_bad
    instr_control.SMUbad_voltage_set(8)
    # Measure VO2 and VCM2
    V2, VO2, VCM2 = instr_control.dmm_measure_x3()
    # print(V2, VO2, VCM2)

    voltage_error = (VO2 - VO1)/(VCM2 - VCM1)

    CMRR = 20*log10(abs(1/voltage_error)) + 20*log10(50)
    # CMRR = 0

    # voltage_error, CMRR = 2.464561578, 103.45404042412

    return voltage_error, CMRR
