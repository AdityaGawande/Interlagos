import csv_utils
import binary_utils
from i2c_data_tx_util import testmode_entry, testmode_exit, i2c_reg_write
from gsheet_util import update_local_files
import pyvisa

# Variables
# sleep time for visa commands
t = 0.01
# Name of the local file where the sheet is downloaded
filename_csv = 'gsheet_trimbit_values.csv'
# Taken from the URL
google_sheet_id = '1hF4Snpfwg6-8w03q6VBuWfcwUNAFX5iWZxPIyqwjrc4'
# Name of the sheet (not the overall spreadsheet)
google_sheetname = 'Python_sheet'



while True:
    print("1 for testmode entry")
    print("2 for trimbit dumping")
    print("3 for testmode exit")
    print("4 for trimbit value update")
    
    user_input_str = input("Enter a number (1, 2, 3, 4) or 0/q to quit: ")
    choice = int(user_input_str)

    if choice == 1:
        # enter testmode
        print("testmode_entry")
        testmode_entry(t)
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
    else:
        print("Invalid choice!")

    if user_input_str.lower() in ['0', 'q']:
        print("Exiting...")
        break
    else:
        print("Please enter a valid number.")