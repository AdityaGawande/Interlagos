# Move all of this code in Tn_wrappers and trimming_tests. S3 should be the old S4


# This should update data from google sheet
# Enter testmode and wait to verify that testmode has been activated
# Measure voltage at VREF using the same SMU
# Write bits to the chip and verify that bits have been changed
# Exit testmode
# Measure gain/cmrr based on user input for n times
# Update value into google sheet (manually)
# Loopback

# Bugs -
# 
# Change instrument for VREF and IN+/IN-
# Turn instruments on and off in the init portion (atleast keep a note of it)

import sources.i2c as i2c
import sources.gsheet_util as gsheet_util
# import instr_top
import time
import sources.instr_control as instr_control
from sources.constants import G0 as Gain_ideal
import standard_tests

# Options -
# 1. Update trimbit values from sheet - all values (enter testmode, write bits and exit. Ask for ACK before each step)

# Measure gain 10 times
# Update trim values
# Measure gain 10 times

# testmode_entry_exit_check replaces this
def testmode_entry_exit_check():
    # print("Updating values from Google sheet...")
    gsheet_util.csv_file_update()
    # input("Press Enter to enter test mode...")
    # print("Entering test mode...")
    # i2c.testmode_entry_debug() # Update this function - change instrument for vref and vsense connection
    # input("Press Enter to write trim bits from sheet...")
    # print("Writing trim bits...")
    # i2c.trimbits_dump_res()
    
    
    
    instr_control.SMUbad_voltage_set(8)
    i2c.testmode_entry_debug()
    time.sleep(0.5)
    instr_control.SMUbad_shutdown()
    instr_control.Testmode_current_check()
    instr_control.dmm_measure_clk()
    i2c.testmode_VBG()
    time.sleep(2)
    instr_control.dmm_measure_vbg()
    # Measure VBG value here
    # Measure supply current here
    i2c.testmode_exit()
    instr_control.Amplifier_current_check()
    # input("Change the VBG trimbit?")
    # Measure supply current here
    # i2c.testmode_VBG()
    # i2c.testmode_CLK()




    # i2c.trimbits_dump_osc_core()
    # i2c.trimbits_dump()

    # input("Press Enter to exit test mode...")
    # print("Exiting test mode...")
    # i2c.testmode_exit()
    # instr_top.honest_to_god_cmrr_init() # Does this have to be removed?


def VBG_trimbit_trial(trimvalue):
    gsheet_util.write_value('B2', trimvalue)
    print(f"VBG trimbit changed to {trimvalue}")
    # Read values from python sheet
    gsheet_util.csv_file_update()
    # Write values into the chip (first two registers)
    i2c.trimbits_dump_vbg()
    time.sleep(1)
    i2c.testmode_VBG()
    time.sleep(1)
    instr_control.dmm_measure_vbg()
    instr_control.dmm_measure_vbg()
    instr_control.dmm_measure_vbg()
    instr_control.dmm_measure_vbg()
    instr_control.dmm_measure_vbg()

def VBG_trimcode_shortcut(trimvalue):
    gsheet_util.write_value('B2', trimvalue)
    print(f"VBG trimbit changed to {trimvalue}")
    # Read values from python sheet
    gsheet_util.csv_file_update()
    # Write values into the chip (first two registers)
    i2c.trimbits_dump_vbg()
    time.sleep(1)
    i2c.trimbits_dump_vbg()
    time.sleep(1)
    i2c.testmode_VBG()
    time.sleep(1)
    i2c.testmode_VBG()
    time.sleep(1)
    # instr_control.SMUbad_voltage_set(2)
    # instr_control.CLK_DC_voltage_set(2.038)
    # instr_control.SMUchA_voltage_set(2)
    instr_control.dmm_measure_vbg()
    instr_control.dmm_measure_vbg()

def VBG_trimcode_shortcut_silent(trimvalue):
    gsheet_util.write_value('B2', trimvalue)
    print(f"VBG trimbit changed to {trimvalue}")
    # Read values from python sheet
    gsheet_util.csv_file_update()
    # Write values into the chip (first two registers)
    i2c.trimbits_dump_vbg()
    time.sleep(1)
    i2c.trimbits_dump_vbg()
    time.sleep(1)
    i2c.testmode_VBG()
    time.sleep(1)
    i2c.testmode_VBG()
    time.sleep(1)
    # instr_control.SMUbad_voltage_set(2)
    # instr_control.CLK_DC_voltage_set(2.038)
    # instr_control.SMUchA_voltage_set(2)
    # instr_control.dmm_measure_vbg()
    # instr_control.dmm_measure_vbg()

def VBG_stability():
    instr_control.SMUbad_voltage_set(8)
    i2c.testmode_entry_debug()
    time.sleep(0.5)
    instr_control.SMUbad_shutdown()
    instr_control.Testmode_current_check()
    instr_control.dmm_measure_clk()
    i2c.testmode_VBG()
    time.sleep(2)

    trimvalue = 0
    VBG_trimbit_trial(trimvalue)
    # trimvalue = 1
    # VBG_trimbit_trial(trimvalue)
    trimvalue = 4
    VBG_trimbit_trial(trimvalue)
    trimvalue = 12
    VBG_trimbit_trial(trimvalue)
    # trimvalue = 13
    # gsheet_util.write_value('B2', trimvalue)
    # print(f"VBG trimbit changed to {trimvalue}")
    # # Read values from python sheet
    # gsheet_util.csv_file_update()
    # # Write values into the chip (first two registers)
    # i2c.trimbits_dump_vbg()
    # time.sleep(1)
    # instr_control.dmm_measure_vbg()
    # instr_control.dmm_measure_vbg()
    # instr_control.dmm_measure_vbg()
    # instr_control.dmm_measure_vbg()
    # instr_control.dmm_measure_vbg()

    # Measure VBG value here
    # Measure supply current here
    i2c.testmode_exit()
    instr_control.Amplifier_current_check()

# Deprecated. Use i2c.testmode_entry_v2 instead
def testmode_entry_shortcut():
    instr_control.SMUbad_voltage_set(8)
    i2c.testmode_entry_debug()
    time.sleep(0.5)
    i2c.testmode_entry_debug()
    time.sleep(0.5)
    instr_control.SMUbad_shutdown()

def VBG_trim():
    # print("Updating values from Google sheet...")
    # gsheet_util.csv_file_update()
    # input("Press Enter to enter test mode...")
    # print("Entering test mode...")
    # i2c.testmode_entry_debug() # Update this function - change instrument for vref and vsense connection
    # input("Press Enter to write trim bits from sheet...")
    # print("Writing trim bits...")
    # i2c.trimbits_dump_res()
    
    
    
    instr_control.SMUbad_voltage_set(8)
    i2c.testmode_entry_debug()
    time.sleep(0.5)
    instr_control.SMUbad_shutdown()
    instr_control.Testmode_current_check()
    instr_control.dmm_measure_clk()
    i2c.testmode_VBG()
    time.sleep(2)

    trimvalue = 8
    while (trimvalue < 32):
        gsheet_util.write_value('B2', trimvalue)
        print(f"VBG trimbit changed to {trimvalue}")
        # Read values from python sheet
        gsheet_util.csv_file_update()
        # Write values into the chip (first two registers)
        i2c.trimbits_dump_vbg()
        time.sleep(1)
        instr_control.dmm_measure_vbg()
        instr_control.dmm_measure_vbg()
        instr_control.dmm_measure_vbg()
        instr_control.dmm_measure_vbg()
        instr_control.dmm_measure_vbg()
        trimvalue = trimvalue + 1

    # Measure VBG value here
    # Measure supply current here
    i2c.testmode_exit()
    instr_control.Amplifier_current_check()

def IREF_trim():
    # print("Updating values from Google sheet...")
    gsheet_util.csv_file_update()
    instr_control.SMUbad_voltage_set(8)

    i2c.testmode_entry_debug()
    time.sleep(0.5)
    i2c.testmode_entry_debug()
    time.sleep(0.5)
        

    instr_control.SMUbad_shutdown()
    instr_control.Testmode_current_check()
    instr_control.dmm_measure_clk()

    i2c.trimbits_dump_vbg()
    time.sleep(1)
    i2c.trimbits_dump_vbg()
    time.sleep(1)
        
    i2c.testmode_IREF()
    instr_control.CLK_DC_voltage_set(2)
    instr_control.SMUchA_voltage_set(2)
    time.sleep(2)

    trimvalue = 0
    while (trimvalue < 32):
        gsheet_util.write_value('B4', trimvalue)
        print(f"IREF trimbit changed to {trimvalue}")
        # Read values from python sheet
        gsheet_util.csv_file_update()
        # Write values into the chip (first two registers)
        i2c.trimbits_dump_iref()
        time.sleep(1)
        i2c.trimbits_dump_iref()
        time.sleep(1)
        instr_control.SMUbad_voltage_set(2)
        instr_control.CLK_DC_voltage_set(2.038)
        instr_control.SMUchA_voltage_set(2)
        time.sleep(1)
        instr_control.dmm_measure_IREF()
        instr_control.dmm_measure_IREF()
        instr_control.dmm_measure_IREF()
        instr_control.dmm_measure_IREF()
        instr_control.dmm_measure_IREF()

        instr_control.SMUbad_shutdown()
        trimvalue = trimvalue + 4

    # Measure VBG value here
    # Measure supply current here
    i2c.testmode_exit()
    instr_control.Amplifier_current_check()

def IREF_trimcode_shortcut(trimvalue):
    gsheet_util.write_value('B4', trimvalue)
    print(f"IREF trimbit changed to {trimvalue}")
    # Read values from python sheet
    gsheet_util.csv_file_update()
    # Write values into the chip (first two registers)
    i2c.trimbits_dump_iref()
    time.sleep(1)
    i2c.trimbits_dump_iref()
    time.sleep(1)
    instr_control.SMUbad_voltage_set(2)
    instr_control.CLK_DC_voltage_set(2.038)
    instr_control.SMUchA_voltage_set(2)
    instr_control.dmm_measure_IREF()
    instr_control.dmm_measure_IREF()

def IREF_stability():
    IREF_trimcode_shortcut(27)
    IREF_trimcode_shortcut(28)

def VBG_testmode_exit_stability():
    i = 17
    while(i < 32):
        instr_control.VSUP_voltage_reset(2)
        testmode_entry_shortcut()
        VBG_trimcode_shortcut_silent(15)
        VBG_trimcode_shortcut_silent(16)
        VBG_trimcode_shortcut(i)
        instr_control.Testmode_current_check()

        i2c.testmode_exit()
        i2c.testmode_exit()
        instr_control.Amplifier_current_check()
        i = i+1

def CLK_trimcode_shortcut(osc_sel,trimvalue):
    # osc_sel = 0
    gsheet_util.write_value('B6', osc_sel)
    print(f"CLK_freq_sel trimbit changed to {osc_sel}")
    gsheet_util.write_value('B5', trimvalue)
    print(f"OSC_accuracy trimbit changed to {trimvalue}")
    # Read values from python sheet
    gsheet_util.csv_file_update()
    # Write values into the chip (first two registers)
    i2c.trimbits_dump_clk()
    time.sleep(1)
    i2c.trimbits_dump_clk()
    time.sleep(1)
    i2c.testmode_CLK()
    time.sleep(1)
    i2c.testmode_CLK()
    time.sleep(1)
    # instr_control.SMUbad_voltage_set(2)
    # instr_control.CLK_DC_voltage_set(2.038)
    # instr_control.SMUchA_voltage_set(2)
    instr_control.dmm_measure_clk()
    instr_control.dmm_measure_clk()

def CLK_trim_starter():
    instr_control.VSUP_voltage_reset(2)
    testmode_entry_shortcut()
    VBG_trimcode_shortcut(1)
    VBG_trimcode_shortcut(2)
    VBG_trimcode_shortcut(4)
    VBG_trimcode_shortcut(8)
    VBG_trimcode_shortcut(9)
    VBG_trimcode_shortcut(10)
    VBG_trimcode_shortcut(11)
    VBG_trimcode_shortcut(12)
    # VBG_trimcode_shortcut(13)
    # VBG_trimcode_shortcut(14)

    # VBG_trimcode_shortcut(12)
    i2c.testmode_IREF()
    instr_control.SMUbad_voltage_set(2)
    instr_control.CLK_DC_voltage_set(2.038)
    instr_control.SMUchA_voltage_set(2)
    time.sleep(1)
    instr_control.dmm_measure_IREF()
    time.sleep(1)
    instr_control.SMUbad_shutdown()
    i2c.testmode_VBG()
    time.sleep(1)
    instr_control.dmm_measure_vbg()
    # i2c.testmode_exit()
    # input("Check VBG")
    i2c.testmode_exit()
    i2c.testmode_exit()
    input("Testmode should be off.")
    testmode_entry_shortcut()
    i2c.testmode_VBG()
    i2c.testmode_VBG()
    input("Check VBG")
    # i2c.testmode_IREF()
    # i2c.testmode_IREF()
    # input("Check VBG")
    # IREF_trimcode_shortcut(27)
    # input("Check current here")
    # IREF_trimcode_shortcut(16)
    # input("Check current here")
    # IREF_trimcode_shortcut(31)
    # input("Check current here")
    # instr_control.SMUbad_shutdown()
    # print("Dummy statement to make sure interpreter does not freak out")

def CLK_trim_starter_fastmode():
    print("Write some code here")

standard_tests.Starter()

CLK_trim_starter()

# CLK_trimcode_shortcut(4,0)
# CLK_trimcode_shortcut(4,32)
# CLK_trimcode_shortcut(4,33)
CLK_trimcode_shortcut(4,63)

# i2c.testmode_exit()
# i2c.testmode_exit()

# i = 0
# while(i < 64):
#     CLK_trimcode_shortcut(i)
#     i = i + 8

# while
# instr_control.VSUP_voltage_reset(2)
# IREF_trim()

# length = 3
# PLC = 100
# standard_tests.gain_error_measurement(length, Gain_ideal, PLC)
# print()
# i = 10
# while(i):
#     testmode_entry_exit_check()
#     i = i-1

# VBG_trim()
# IREF_trim()
# i = 10
# while(i):
#     VBG_stability()
#     i = i-1

# length = 3 
# PLC = 100
# standard_tests.gain_error_measurement(length, Gain_ideal, PLC)
# print()