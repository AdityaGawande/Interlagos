from datetime import datetime
import time
import sources.instr_control as instr_control
import sources.i2c as i2c
import sources.gsheet_util as gsheet_util
from sources.constants import *

def isTestmodeActive():
    
    # time.sleep(2)
    # i2c.testmode_CLK()
    # time.sleep(2)
    # clk = instr_control.dmm_measure_clk()
    # print(f"Clock frequency = {clk:.0f}")
    answer = int(input("Testmode active? -"))
    if(answer == 1):
        return True
    else:
        return False
    # if (clk > 50):
    #     return True
    # else:
    #     return False

def isVBG_Visible():
    # Check if voltage at VREF is greater than 0.9V
    # Check if clock frequency at VREF is 0
    print("Code to be written here")

def testmode_entry_safe():
    # Enter testmode
    i2c.testmode_entry_v2()
    fails = 0
    while(isTestmodeActive()==False):
        fails = fails + 1
        i2c.testmode_entry_v2()
        if(fails > 1):
            print("Testmode entry failed. Retrying")
            time.sleep(1)
            # instr_control.instrument_check()
            time.sleep(2)
        if(fails > 20):
            gsheet_util.email_sender("Testmode entry failed")
            raise ValueError("Testmode entry failed after 20 tries")

def testmode_exit_safe():
    # Exit testmode
    i2c.testmode_exit()
    fails = 0
    while(isTestmodeActive()==True):
        fails = fails + 1
        i2c.testmode_exit()
        if(fails > 1):
            print("Testmode exit failed. Retrying")
            time.sleep(1)
            # instr_control.instrument_check()
            time.sleep(2)
        if(fails > 20):
            gsheet_util.email_sender("Testmode exit failed")
            raise ValueError("Testmode exit failed after 20 tries")

def testmode_entry_exit_check(total_turns=1000, fresh=1):
    if(fresh==1):
        instr_control.VSUP_voltage_reset(active_chip_slot)
    n = 0
    fails = 0
    for i in range (0,total_turns):
        fail = 0
        # i2c.testmode_entry_v2()
        testmode_entry_safe()
        if(isTestmodeActive() == False):
            print("Testmode entry unsuccessful")
            fail = 1
            fails = fails+1
        # i2c.testmode_exit()
        testmode_exit_safe()
        if(isTestmodeActive() == True):
            print("Testmode exit unsuccessful. Resetting chip supply.")
            instr_control.VSUP_voltage_reset(2)
            fail = 1
            fails = fails+1
        # if(fail == 0):
        #     print("Entry-exit loop was successful")
        n = n+1
        print(f"Success rate = {n-fails}/{n}")

def set_vbg_trim(trimvalue):
    gsheet_util.write_value(VBG_cell, trimvalue)

def set_vbgtc_trim(trimvalue):
    gsheet_util.write_value(VBGTC_cell, trimvalue)

def set_iref_trim(trimvalue):
    gsheet_util.write_value(IREF_cell, trimvalue)

def set_clk_trim(trimvalue):
    gsheet_util.write_value(OSC_cell, trimvalue)

def set_clk_sel_trim(trimvalue):
    gsheet_util.write_value(CHOP_FREQ_cell, trimvalue)


def VBG_trimbit_push(trimvalue):
    set_vbg_trim(trimvalue)
    gsheet_util.csv_file_update(silent=1)
    i2c.trimbits_dump_vbg()
    time.sleep(0.3)
    voltage = instr_control.dmm_measure_vbg(report=0)
    print(f"{trimvalue},\t{voltage:.6f}")

def VBG_trim_init():
    # instr_control.VSUP_voltage_reset(active_chip_slot)
    # Reset the values of OSC, VBGTC and IREF
    set_iref_trim(31)
    set_vbgtc_trim(16)
    set_clk_trim(31)
    set_clk_sel_trim(0)
    
    # Enter testmode
    testmode_entry_safe()
    
    # Change visibility mode to VBG
    i2c.testmode_VBG()
    print("VBG trimming")

def VBG_trim_flow():
    VBG_trim_init()
    for i in range(10,15):
        for j in range(0,i+1):
            VBG_trimbit_push(j)
        testmode_entry_exit_check(10,0)
        testmode_entry_safe()
    print("Testmode is active")
    

def IREF_trimbit_push(trimvalue):
    set_iref_trim(trimvalue)
    gsheet_util.csv_file_update(silent=1)
    i2c.trimbits_dump_iref()
    # instr_control.IREF_read_setup()
    # time.sleep(0.3)
    # current1 = (instr_control.dmm_measure_iref(report=0))*float(1000*1000*1000)
    # current2 = (instr_control.dmm_measure_iref(report=0))*float(1000*1000*1000)
    # current3 = (instr_control.dmm_measure_iref(report=0))*float(1000*1000*1000)
    # current4 = (instr_control.dmm_measure_iref(report=0))*float(1000*1000*1000)
    # current5 = (instr_control.dmm_measure_iref(report=0))*float(1000*1000*1000)
    input("Check current on the SMU")
    instr_control.SMU_shutdown()

    # print(f"{trimvalue},\t{current1:.0f},\t{current2:.0f},\t{current3:.0f},\t{current4:.0f},\t{current5:.0f}")

def IREF_trim_init(vbg_final_trimbit):
    # Reset the values of OSC, VBGTC and IREF
    instr_control.VSUP_voltage_reset(active_chip_slot)
    set_vbg_trim(vbg_final_trimbit)
    # set_iref_trim(16)
    set_iref_trim(0)
    set_vbgtc_trim(16)
    set_clk_trim(31)
    set_clk_sel_trim(0)
    
    # Enter testmode
    testmode_entry_safe()
    i2c.testmode_VBG()
    # Gradually step up to the VBG value
    for j in range(0,vbg_final_trimbit):
        VBG_trimbit_push(j)
    # VBG_trimbit_push(vbg_final_trimbit)
    
    # Change visibility mode to VBG
    i2c.testmode_IREF()
    input("Wait and check chip status here")
    print("IREF trimming")

def IREF_trim_flow(vbg_final_trimbit):
    IREF_trim_init(vbg_final_trimbit)
    for i in range(0,31):
        IREF_trimbit_push(i)
        testmode_exit_safe()
        instr_control.Amplifier_current_check()
        testmode_entry_safe()
        i2c.testmode_IREF()
    print("Testmode is active")


def CLK_trim_init(vbg_final_trimbit, iref_final_trimbit):
    # Reset the values of OSC, VBGTC and IREF
    instr_control.VSUP_voltage_reset(active_chip_slot)
    set_vbg_trim(vbg_final_trimbit)
    # set_iref_trim(16)
    set_iref_trim(iref_final_trimbit)
    set_vbgtc_trim(16)
    set_clk_trim(0)
    set_clk_sel_trim(0)
    
    # Enter testmode
    testmode_entry_safe()
    i2c.testmode_VBG()
    for i in range(0,vbg_final_trimbit+1):
        VBG_trimbit_push(i)
    IREF_trimbit_push(iref_final_trimbit)
    instr_control.Amplifier_current_check()
    # Change visibility mode to VBG
    i2c.testmode_CLK()
    input("Wait and check chip status here")
    print("CLK trimming")

def CLK_trimbit_push(trimvalue):
    set_clk_trim(trimvalue)
    gsheet_util.csv_file_update(silent=1)
    i2c.trimbits_dump_clk()
    # instr_control.IREF_read_setup()
    time.sleep(0.3)
    freq1 = (instr_control.dmm_measure_clk(report=0))
    freq2 = (instr_control.dmm_measure_clk(report=0))
    freq3 = (instr_control.dmm_measure_clk(report=0))
    freq4 = (instr_control.dmm_measure_clk(report=0))
    freq5 = (instr_control.dmm_measure_clk(report=0))
    
    # instr_control.SMU_shutdown()
    print(f"{trimvalue},\t{freq1:.0f},\t{freq2:.0f},\t{freq3:.0f},\t{freq4:.0f},\t{freq5:.0f}")

def CLK_trim_flow(vbg_final_trimbit,iref_final_trimbit):
    CLK_trim_init(vbg_final_trimbit,iref_final_trimbit)
    for i in range(0,13):
        CLK_trimbit_push(i)
    set_clk_sel_trim(6)
    CLK_trimbit_push()
    print("Testmode is active")

def testmode_exit_entry_loop_single():
    testmode_exit_safe()
    # instr_control.Amplifier_current_check()
    testmode_entry_safe() 

def trim_check(vbg_t,iref_t,clk_t,clk_sel_t):
    instr_control.VSUP_voltage_reset(active_chip_slot)
    set_vbg_trim(vbg_t)
    # set_iref_trim(16)
    set_iref_trim(16)
    set_vbgtc_trim(16)
    set_clk_trim(31)
    set_clk_sel_trim(6)
    
    # Enter testmode
    testmode_entry_safe()
    # Gradually step up to the VBG value
    print("Writing VBG bits")
    # for j in range(0,vbg_t+1):
    #     i2c.testmode_VBG()
    #     VBG_trimbit_push(j)
    #     testmode_exit_entry_loop_single()    
    
    i2c.testmode_VBG()
    VBG_trimbit_push(1)
    VBG_trimbit_push(3)
    VBG_trimbit_push(7)
    testmode_exit_entry_loop_single()
    
    # Writing IREF bits
    print("Writing IREF bits")
    # i2c.testmode_IREF()
    IREF_trimbit_push(iref_t)
    testmode_exit_entry_loop_single()
    
    # Writing CLK bits
    print("Writing CLK bits")
    CLK_trimbit_push(clk_t)
    # testmode_exit_entry_loop_single()
    
    # Writing CLK sel bits
    # print("Writing CLK sel bits")
    # set_clk_sel_trim(clk_sel_t)
    # CLK_trimbit_push(clk_t)
    # testmode_exit_entry_loop_single()

def error_check():
    print("This still gets printed")
    raise ValueError("This throws an error and stops the program")

def Starter():
    now = str(datetime.now())
    print("Test started at", now)
    print(f"Attempting Trimming on chip #{active_chip_id} placed at slot #{active_chip_slot}")
    print()
    
def Desert():
    print()
    now = str(datetime.now())
    print("Test completed at", now)
    print(f"Attempted Trimming on chip #{active_chip_id} placed at slot #{active_chip_slot}")