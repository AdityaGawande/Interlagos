import csv_utils
import binary_utils
from i2c_data_tx_util import testmode_entry, testmode_exit, i2c_reg_write
from gsheet_util import update_local_files
import pyvisa
from visa_pwr_update_util import testmode_pwr_set, testmode_pwr_ref_reset, vref_set
from visa_smu_turnoff import turn_off_smu_output
import time
import relay_power_control


# Variables
# sleep time for visa commands
t = 0.05
# Name of the local file where the sheet is downloaded
filename_csv = 'gsheet_trimbit_values.csv'
# Taken from the URL
google_sheet_id = '1hF4Snpfwg6-8w03q6VBuWfcwUNAFX5iWZxPIyqwjrc4'
# Name of the sheet (not the overall spreadsheet)
google_sheetname = 'Python_sheet'

def testmode_entry_macro(t):
    # enter testmode
    # print("Disconnecting Vsense resistor")
    # relay_power_control.vsense_res_disconnect()

    # print("Changing supply voltage")
    ##turn_off_smu_output()
    testmode_pwr_set()
    print("testmode_entry")
    time.sleep(1)
    testmode_entry(t)
    #testmode_pwr_ref_reset()
    #turn_off_smu_output()
    #testmode_entry(t)

def trimbits_writing_macro(filename_csv, t):
    # write all bits
    # print("testmode_entry")
    # testmode_entry()
    # Write a for loop which goes through all 9 registers and writes data
    # for
        # print(f"writing reg{i}")
    #     i2c_reg_write()

    parameters = csv_utils.read_csv_with_bit_length(filename_csv)
    for param in parameters:
        parameters[param]['current'] = parameters[param]['default']
    updated_params = parameters

    # print("\nUsing values in main:")
    # for param, data in updated_params.items():
    #     print(f"{param}: {data['current']}")

    bit_arrays = binary_utils.generate_fixed_length_binary_arrays(updated_params)

    # print(bit_arrays)

    regf2 = bit_arrays['regf2']
    # print("fresh regf2 is ", end="")
    # print(regf2)
    efuse_prog_enable_bits = bit_arrays['efuse_prog_enable']
    efuse_reload_bits = bit_arrays['efuse_reload']
    pwr_5v_enable_bits = bit_arrays['pwr_5v_enable']
    regff = 5*[1] + pwr_5v_enable_bits + efuse_reload_bits + efuse_prog_enable_bits

    # regs = [bit_arrays[f'reg0{i}'] for i in range(8)]

    regs = [bit_arrays[f'reg0{i}'] for i in range(8)] + [regf2] + [regff]

    for i in range(0,10):
        print(f"{i} = ",regs[i])

    # i2c_reg_write(0, regs[0], t)
    # i2c_reg_write(8, regs[8], t)

    for i in range(0,9):
        print(f"Writing into reg {i}")
        i2c_reg_write(i, regs[i], t)

def trimbits_writing_macro_single(filename_csv, t, regnum):
    # write all bits
    # print("testmode_entry")
    # testmode_entry()
    # Write a for loop which goes through all 9 registers and writes data
    # for
        # print(f"writing reg{i}")
    #     i2c_reg_write()

    parameters = csv_utils.read_csv_with_bit_length(filename_csv)
    for param in parameters:
        parameters[param]['current'] = parameters[param]['default']
    updated_params = parameters

    # print("\nUsing values in main:")
    # for param, data in updated_params.items():
    #     print(f"{param}: {data['current']}")

    bit_arrays = binary_utils.generate_fixed_length_binary_arrays(updated_params)

    # print(bit_arrays)

    regf2 = bit_arrays['regf2']
    # print("fresh regf2 is ", end="")
    # print(regf2)
    efuse_prog_enable_bits = bit_arrays['efuse_prog_enable']
    efuse_reload_bits = bit_arrays['efuse_reload']
    pwr_5v_enable_bits = bit_arrays['pwr_5v_enable']
    regff = 5*[1] + pwr_5v_enable_bits + efuse_reload_bits + efuse_prog_enable_bits

    # regs = [bit_arrays[f'reg0{i}'] for i in range(8)]

    regs = [bit_arrays[f'reg0{i}'] for i in range(8)] + [regf2] + [regff]

    i = regnum

    print(f"{i} = ",regs[i])

    # i2c_reg_write(0, regs[0], t)
    # i2c_reg_write(8, regs[8], t)


    print(f"Writing into reg {i}")
    i2c_reg_write(i, regs[i], t)

def testmode_exit_macro(t):
    # exit testmode
    print("testmode_exit")
    testmode_exit(t)

    # print("Connecting Vsense resistor")
    # relay_power_control.vsense_res_connect()

def gsheet_trimbit_update():
    # Google Sheet ID and mapping of sheet names to local files
    SHEET_ID = google_sheet_id  # Replace with your Google Sheet ID
    FILE_MAP = {
        google_sheetname: filename_csv
        # Add more sheets and files as needed
    }
    # refresh values from google sheet
    update_local_files(SHEET_ID, FILE_MAP)
    parameters = csv_utils.read_csv_with_bit_length(filename_csv)
    for param in parameters:
        parameters[param]['current'] = parameters[param]['default']
    updated_params = parameters

    # print("\nUsing values in main:")
    # for param, data in updated_params.items():
    #     print(f"{param}: {data['current']}")

    bit_arrays = binary_utils.generate_fixed_length_binary_arrays(updated_params)

    # print(bit_arrays)

    regf2 = bit_arrays['regf2']
    # print("fresh regf2 is ", end="")
    # print(regf2)
    efuse_prog_enable_bits = bit_arrays['efuse_prog_enable']
    efuse_reload_bits = bit_arrays['efuse_reload']
    pwr_5v_enable_bits = bit_arrays['pwr_5v_enable']
    regff = 5*[1] + pwr_5v_enable_bits + efuse_reload_bits + efuse_prog_enable_bits

    # regs = [bit_arrays[f'reg0{i}'] for i in range(8)]

    regs = [bit_arrays[f'reg0{i}'] for i in range(8)] + [regf2] + [regff]

    for i in range(0,10):
        print(f"{i} = ",regs[i])
    # print("regf2 is ", end="")
    # print(regs[8])
    # print("regff is ", end="")
    # print(regs[9]) 

while True:
    print("1 for testmode entry")
    print("2 for trimbit dumping")
    print("3 for testmode exit")
    print("4 for trimbit value update")
    print("5 for dac3 resistor code dump")
    print("6 for vcm=0.2V mode")
    print("7 for vcm=1.2V mode")
    print("8 for clock+iref+dac3 code dump")
    
    user_input_str = input("Enter a number (1, 2, 3, 4, 5, 6, 7, 8) or 0/q to quit: ")
    choice = int(user_input_str)

    if choice == 1:
        # enter testmode
        print("Disconnecting Vsense resistor")
        #relay_power_control.vsense_res_disconnect()

        print("Changing supply voltage")
       # turn_off_smu_output()
        testmode_pwr_set()
        print("testmode_entry")
        time.sleep(5)
        testmode_entry(t)
        testmode_pwr_ref_reset()
        #turn_off_smu_output()
        #testmode_entry(t)
        
    elif choice == 2:
        # write all bits
        # print("testmode_entry")
        # testmode_entry()
        # Write a for loop which goes through all 9 registers and writes data
        # for
            # print(f"writing reg{i}")
        #     i2c_reg_write()

        parameters = csv_utils.read_csv_with_bit_length(filename_csv)
        for param in parameters:
            parameters[param]['current'] = parameters[param]['default']
        updated_params = parameters

        # print("\nUsing values in main:")
        # for param, data in updated_params.items():
        #     print(f"{param}: {data['current']}")

        bit_arrays = binary_utils.generate_fixed_length_binary_arrays(updated_params)

        # print(bit_arrays)

        regf2 = bit_arrays['regf2']
        # print("fresh regf2 is ", end="")
        # print(regf2)
        efuse_prog_enable_bits = bit_arrays['efuse_prog_enable']
        efuse_reload_bits = bit_arrays['efuse_reload']
        pwr_5v_enable_bits = bit_arrays['pwr_5v_enable']
        regff = 5*[1] + pwr_5v_enable_bits + efuse_reload_bits + efuse_prog_enable_bits

        # regs = [bit_arrays[f'reg0{i}'] for i in range(8)]

        regs = [bit_arrays[f'reg0{i}'] for i in range(8)] + [regf2] + [regff]

        for i in range(0,10):
            print(f"{i} = ",regs[i])

        # i2c_reg_write(0, regs[0], t)
        # i2c_reg_write(8, regs[8], t)

        for i in range(0,9):
            print(f"Writing into reg {i}")
            i2c_reg_write(i, regs[i], t)

    elif choice == 3:
        # exit testmode
        print("testmode_exit")
        testmode_exit(t)

        print("Connecting Vsense resistor")
        relay_power_control.vsense_res_connect()
    elif choice == 4:
        # Google Sheet ID and mapping of sheet names to local files
        SHEET_ID = google_sheet_id  # Replace with your Google Sheet ID
        FILE_MAP = {
            google_sheetname: filename_csv
            # Add more sheets and files as needed
        }
        # refresh values from google sheet
        update_local_files(SHEET_ID, FILE_MAP)
        parameters = csv_utils.read_csv_with_bit_length(filename_csv)
        for param in parameters:
            parameters[param]['current'] = parameters[param]['default']
        updated_params = parameters

        # print("\nUsing values in main:")
        # for param, data in updated_params.items():
        #     print(f"{param}: {data['current']}")

        bit_arrays = binary_utils.generate_fixed_length_binary_arrays(updated_params)

        # print(bit_arrays)

        regf2 = bit_arrays['regf2']
        # print("fresh regf2 is ", end="")
        # print(regf2)
        efuse_prog_enable_bits = bit_arrays['efuse_prog_enable']
        efuse_reload_bits = bit_arrays['efuse_reload']
        pwr_5v_enable_bits = bit_arrays['pwr_5v_enable']
        regff = 5*[1] + pwr_5v_enable_bits + efuse_reload_bits + efuse_prog_enable_bits

        # regs = [bit_arrays[f'reg0{i}'] for i in range(8)]

        regs = [bit_arrays[f'reg0{i}'] for i in range(8)] + [regf2] + [regff]

        for i in range(0,10):
            print(f"{i} = ",regs[i])
        # print("regf2 is ", end="")
        # print(regs[8])
        # print("regff is ", end="")
        # print(regs[9])
    elif choice == 5:

        gsheet_trimbit_update()
        print("Testmode entry")
        testmode_entry_macro(t)
        print("Writing DAC3 values")
        trimbits_writing_macro_single(filename_csv, t, 2)
        trimbits_writing_macro_single(filename_csv, t, 4)
        print("Exiting testmode")
        testmode_exit_macro(t)

        vref_set(2.5, 1.2)
        




        # # loop ten times
        # for i in range (0,10):

        #     # enter testmode
        #     testmode_entry_macro(t)
        #     # wait on the clock for 5 sec
        #     print(f"Iteration number {i}. Check clock frequency.")
        #     time.sleep(5)

        #     # write bits
        #     trimbits_writing_macro(filename_csv, t)
        #     # exit testmode
        #     testmode_exit_macro(t)
    elif choice == 6:
        vref_set(2.5, 0.2)

    elif choice == 7:
        vref_set(2.5, 1.2)

    elif choice == 8:

        gsheet_trimbit_update()
        print("Testmode entry")
        testmode_entry_macro(t)
        print("Writing clock+current trimbits")
        trimbits_writing_macro_single(filename_csv, t, 0)
        trimbits_writing_macro_single(filename_csv, t, 1)
        trimbits_writing_macro_single(filename_csv, t, 6)
        trimbits_writing_macro_single(filename_csv, t, 7)
        print("Writing DAC3 values")
        trimbits_writing_macro_single(filename_csv, t, 2)
        trimbits_writing_macro_single(filename_csv, t, 4)
        print("Exiting testmode")
        testmode_exit_macro(t)

        vref_set(2.5, 1.2)

    else:
        print("Invalid choice!")

    if user_input_str.lower() in ['0', 'q']:
        print("Exiting...")
        break
    else:
        print("Please enter a valid number.")