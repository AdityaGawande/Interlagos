from datetime import datetime
import sources.instr_control as instr_control
import sources.instr_math as instr_math
# from sources.constants import VCM_low, VCM_high, Isense_high, Isense_low, VREF_voltage, VSUP_typical, VSUP_current_limit
from sources.constants import *

def Starter():
    now = str(datetime.now())
    print("Test started at", now)
    print()

def end_text():
    print()
    now = str(datetime.now())
    print("Test completed at", now)
    print()

def gain_error_measurement_init():
    # Set power supply from this
    instr_control.VSUP_voltage_set(active_chip_slot, VSUP_typical)
    # Set VREF to 2.5V - SMUchA
    instr_control.SMUchA_voltage_set(VCM_low)
    # Set VCM to 0.5V - SMU_bad
    instr_control.SMUbad_voltage_set(VREF_voltage) 

def gain_error_measurement_single(Gain_ideal, dmm1, dmm2, dmm3, iterator):
    # Set Isense_high
    instr_control.SMUchB_current_set(Isense_high)
    # Measure Vsense(V21) and Vout(VO1) at the same time
    V21, VO1, VCM1 = instr_control.dmm_measure_x3_single(dmm1, dmm2, dmm3)

    # Set Isense_low
    instr_control.SMUchB_current_set(Isense_low)
    # Measure Vsense(V22) and Vout(VO2) at the same time
    V22, VO2, VCM2 = instr_control.dmm_measure_x3_single(dmm1, dmm2, dmm3)

    G1 = instr_math.gain_error_standard(V21, VO1, V22, VO2)
    
    print(G1-Gain_ideal, ',' , G1, ',' , V22-V21, ',' , V21, ',' , V22, ',' , VO2-VO1, ',' , VO1, ',' , VO2, ',' , VCM2-VCM1, ',' , VCM1, ',' , VCM2, ',' , str(datetime.now()), iterator+1)

def gain_error_measurement(n, Gain_ideal, PLC):
    print(f"Measuring Gain using the standard method at PLC of {PLC}")
    print()
    
    gain_error_measurement_init()
    dmm1, dmm2, dmm3 = instr_control.dmm_measure_x3_setup()
    
    print("Gain Error, Gain, VDIFF, VDIFF1, VDIFF2, VOUT, VOUT1, VOUT2, VCM, VCM1, VCM2, time, reading_number")
    for i in range(0, n):
        gain_error_measurement_single(Gain_ideal, dmm1, dmm2, dmm3, i)

    instr_control.dmm_measure_x3_deinit(dmm1, dmm2, dmm3)
    instr_control.SMU_shutdown()
    # PSU is not turned off, so that the trim bits are not lost
    
def cmrr_measurement_init():
    # Set power supply from this
    # instr_control.VSUP_voltage_set(VSUP_typical, VSUP_current_limit)
    instr_control.VSUP_voltage_set(active_chip_slot, VSUP_typical)
    # Set VREF to 2.5V - SMUchA
    instr_control.VREF_set(VREF_voltage)
    # instr_control.SMUchA_voltage_set(VREF_voltage)
    # Set Isense to zero
    # input("Recommendation - Inputs should be shorted on the board")
    # instr_control.SMUchB_current_set(0)
    instr_control.Isense_set(0)
    
def cmrr_measurement_single(Gain_ideal, dmm1, dmm2, dmm3, iterator):
    # Set VCM to 0.5V - SMU_bad
    # instr_control.SMUbad_voltage_set(VCM_low)
    instr_control.VCM_set(VCM_low)
    # Measure Vsense(V21) and Vout(VO1) at the same time
    V21, VO1, VCM1 = instr_control.dmm_measure_x3_single(dmm1, dmm2, dmm3)

    # Set VCM to 0.5V - SMU_bad
    # instr_control.SMUbad_voltage_set(VCM_high)
    instr_control.VCM_set(VCM_high)
    # Measure Vsense(V22) and Vout(VO2) at the same time
    V22, VO2, VCM2 = instr_control.dmm_measure_x3_single(dmm1, dmm2, dmm3)

    xy_diff = instr_math.cmrr_standard(VCM1, VO1, VCM2, VO2, Gain_ideal, V21, V22)
    cmrr = instr_math.CMRR_calc(xy_diff)
    print(cmrr, ',' , xy_diff, ',' , V22-V21, ',' , V21, ',' , V22, ',' , VO2-VO1, ',' , VO1, ',' , VO2, ',' , VCM2-VCM1, ',' , VCM1, ',' , VCM2, ',' , str(datetime.now()), ',' , iterator)

def cmrr_measurement(n, Gain_ideal, PLC):
    print(f"Measuring xy_diff using the standard method at PLC of {PLC}")
    print()
    
    cmrr_measurement_init()
    dmm1, dmm2, dmm3 = instr_control.dmm_measure_x3_setup()
    
    print("CMRR, XY_DIFF, VDIFF, VDIFF1, VDIFF2, VOUT, VOUT1, VOUT2, VCM, VCM1, VCM2, time, reading_number")
    for i in range(0, n):
        cmrr_measurement_single(Gain_ideal, dmm1, dmm2, dmm3, i)

    instr_control.dmm_measure_x3_deinit(dmm1, dmm2, dmm3)
    instr_control.SMU_shutdown()
    # PSU is not turned off, so that the trim bits are not lost