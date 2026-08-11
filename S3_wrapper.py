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

import i2c
import gsheet_util
import instr_top
from constants import G0 as Gain_ideal
import standard_tests

# Options -
# 1. Update trimbit values from sheet - all values (enter testmode, write bits and exit. Ask for ACK before each step)

def update_trimbit_values():
    # print("Updating values from Google sheet...")
    # gsheet_util.csv_file_update()
    # input("Press Enter to enter test mode...")
    # print("Entering test mode...")
    # i2c.testmode_entry() # Update this function - change instrument for vref and vsense connection
    # input("Press Enter to write trim bits from sheet...")
    # print("Writing trim bits...")
    # i2c.trimbits_dump_res()
    i2c.testmode_entry_debug()
    # input("Press Enter to exit test mode...")
    # print("Exiting test mode...")
    # i2c.testmode_exit()
    # instr_top.honest_to_god_cmrr_init() # Does this have to be removed?
    
# Measure gain 10 times
# Update trim values
# Measure gain 10 times



standard_tests.Starter()

length = 3
# PLC = 100
# standard_tests.gain_error_measurement(length, Gain_ideal, PLC)
# print()

update_trimbit_values()

length = 3 
# PLC = 100
# standard_tests.gain_error_measurement(length, Gain_ideal, PLC)
# print()
