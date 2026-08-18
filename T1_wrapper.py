# Go through all bits of VBG. Ensure testmode can be exited.

import sources.instr_control as instr_control
import sources.i2c as i2c
import sources.gsheet_util as gsheet_util
from sources.constants import *

def isTestmodeActive():
    current = instr_control.dmm_measure_iq()*float(1000*1000)
    print(f"Current = {current:.3f}")
    if (current > 100):
        return True
    else:
        return False
    
def testmode_entry_exit_check():
    while(True):
        i2c.testmode_entry_v2()
        if(isTestmodeActive() == False):
            print("Testmode entry unsuccessful")    
        i2c.testmode_exit()
        if(isTestmodeActive() == True):
            print("Testmode exit unsuccessful")
        print("Entry-exit loop was successful")
        
def VBG_trimbit_push(trimvalue):
    gsheet_util.write_value(VBG_cell, trimvalue)
    