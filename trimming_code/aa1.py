import pyvisa
import time
from concurrent.futures import ThreadPoolExecutor
import gsheet_util_new  # Assumes you have this utility

import csv_utils
import binary_utils
from i2c_data_tx_util import testmode_entry, testmode_exit, i2c_reg_write
from gsheet_util import update_local_files
import pyvisa
from visa_pwr_update_util import testmode_pwr_set, testmode_pwr_ref_reset
from visa_smu_turnoff import turn_off_smu_output
import time
import relay_power_control

# ===> Constants
vref = 2.5
meas_vol = 0
google_sheet_id = '1hF4Snpfwg6-8w03q6VBuWfcwUNAFX5iWZxPIyqwjrc4'
google_sheetname = 'TC_G50_M1'
google_sheetname2 = 'Python_sheet_M1'

arr1 = [13, 25, 37, 49, 61, 73, 85, 97, 109, 121, 132, 144, 156, 168, 180]

# CM voltage and I_sense for each iteration
cm_v = [0.5, 0.6, 0.5]
isense_v = [0.001, 0.001, 0.002]

# SMU addresses for measurement
smu_address_1 = "USB0::0x05E6::0x2450::04495761::INSTR"
smu_address_2 = "USB0::0x05E6::0x2460::04323817::INSTR"
keithley_2636b_address = 'USB0::0x05E6::0x2636::4428135::INSTR'
function_gen_address = "USB0::0x0957::0x2807::MY58000574::INSTR"
dmm_address = "USB0::0x2A8D::0x1301::MY57210465::INSTR"


# ===> VISA Setup
rm = pyvisa.ResourceManager()

# function generatro setup
gen = rm.open_resource(function_gen_address)
gen.timeout = 5000

# Function to measure and average voltage from SMU
def measure_and_average(smu_address, num_measurements=1):
    smu = rm.open_resource(smu_address)
    smu.timeout = 5000
    smu.write("OUTP ON")
    vaverage = 0.0
    v_all = []
    for i in range(num_measurements):
        smu.write(":SENS:FUNC 'VOLT:DC'")
        smu.write(":SENS:VOLT:DC:AZER ON")
        smu.write(":SENS:VOLT:DC:NPLC 10")
        raw_data = smu.query(":MEAS:VOLT?")
        voltage = float(raw_data.strip())
        #voltage_str = smu.query("MEAS:VOLT?")
        #voltage = float(voltage_str)
        print(f"Measured Voltage {i+1} from {smu_address}: {voltage:.9f} V")
        vaverage += voltage
        v_all.append(voltage)

        time.sleep(0.000001)

    vaverage /= num_measurements
    print(f"\nAverage Voltage from {smu_address}: {vaverage:.9f} V")
    return vaverage, v_all

def measure_dmm (dmm_address):
    dmm = rm.open_resource(dmm_address)
    dmm_v = dmm.query("MEAS:VOLT:DC?")
    print(str(float(dmm_v)), dmm_v)
    return str(float(dmm_v))


j = 0  # measurements selection (0 to 5)
google_sheetname1 = "Python_sheet_M1"
gsheet_util_new.write_single_value(google_sheet_id, google_sheetname1, "B8", 0)
gsheet_util_new.write_single_value(google_sheet_id, google_sheetname1, "B9", 0)

t = 0.01
filename_csv = 'gsheet_trimbit_values.csv'

while j < 1:
    k = 0
    while k < 5:
        """
        0 - testmode entry
        1 - download codes
        2 - trim bots dumping
        3 - testmode exit
        4 - amplification

        """
        if k == 0:
            # enter testmode
            print("Disconnecting Vsense resistor")
            relay_power_control.vsense_res_disconnect()

            print("Changing supply voltage")
            turn_off_smu_output()
            testmode_pwr_set()
            print("testmode_entry")
            time.sleep(5)
            testmode_entry(t)
            testmode_pwr_ref_reset()
            time.sleep(2)

        elif k == 2:
            parameters = csv_utils.read_csv_with_bit_length(filename_csv)
            for param in parameters:
                parameters[param]['current'] = parameters[param]['default']
            updated_params = parameters

            bit_arrays = binary_utils.generate_fixed_length_binary_arrays(updated_params)

            regf2 = bit_arrays['regf2']
            efuse_prog_enable_bits = bit_arrays['efuse_prog_enable']
            efuse_reload_bits = bit_arrays['efuse_reload']
            pwr_5v_enable_bits = bit_arrays['pwr_5v_enable']
            regff = 5*[1] + pwr_5v_enable_bits + efuse_reload_bits + efuse_prog_enable_bits

            regs = [bit_arrays[f'reg0{i}'] for i in range(8)] + [regf2] + [regff]

            for i in range(0,10):
                print(f"{i} = ",regs[i])

            for i in range(0,9):
                print(f"Writing into reg {i}")
                i2c_reg_write(i, regs[i], t)
            time.sleep(2)

        elif k == 3:
            # exit testmode
            print("testmode_exit")
            testmode_exit(t)

            print("Connecting Vsense resistor")
            relay_power_control.vsense_res_connect()

            time.sleep(2)


        elif k == 1:
            # Google Sheet ID and mapping of sheet names to local files
            SHEET_ID = '1hF4Snpfwg6-8w03q6VBuWfcwUNAFX5iWZxPIyqwjrc4'  # Replace with your Google Sheet ID
            
            FILE_MAP = {
                google_sheetname2: filename_csv
                # Add more sheets and files as needed
            }
            # refresh values from google sheet
            update_local_files(SHEET_ID, FILE_MAP)
            parameters = csv_utils.read_csv_with_bit_length(filename_csv)
            for param in parameters:
                parameters[param]['current'] = parameters[param]['default']
            updated_params = parameters

            bit_arrays = binary_utils.generate_fixed_length_binary_arrays(updated_params)

            regf2 = bit_arrays['regf2']
            
            efuse_prog_enable_bits = bit_arrays['efuse_prog_enable']
            efuse_reload_bits = bit_arrays['efuse_reload']
            pwr_5v_enable_bits = bit_arrays['pwr_5v_enable']
            regff = 5*[1] + pwr_5v_enable_bits + efuse_reload_bits + efuse_prog_enable_bits

            regs = [bit_arrays[f'reg0{i}'] for i in range(8)] + [regf2] + [regff]

            for i in range(0,10):
                print(f"{i} = ",regs[i])
            
            time.sleep(2)

        elif k == 4:
        
            for i in range(3):
                cm_voltage = cm_v[i]
                isense = isense_v[i]

                print(f"\nIteration {i+1} - CM Voltage: {cm_voltage}, Isense: {isense}")

                # --- Configure Keithley 2636B ---
                smu = rm.open_resource(keithley_2636b_address)
                smu.write("*RST")
                time.sleep(1)

                smu.write("smub.source.func = smub.OUTPUT_DCAMPS")
                smu.write(f"smub.source.leveli = {isense}")
                smu.write("smub.source.limitv = 10")
                smu.write("smub.source.output = smub.OUTPUT_ON")

                smu.write("smua.source.func = smua.OUTPUT_DCVOLTS")
                smu.write(f"smua.source.levelv = {vref}")
                smu.write("smua.source.limiti = 0.0005")
                smu.write("smua.source.output = smub.OUTPUT_ON")
                smu.close()

                # Configure Function Generator
                gen.write("OUTPut OFF")
                gen.write("FUNCtion:SHAPe DC")
                gen.write(f"SOUR1:VOLT:OFFS {cm_voltage}")
                gen.write("OUTPut ON")
                time.sleep(5)

                # Measure Voltages from SMUs
                with ThreadPoolExecutor() as executor:
                    futures = [
                        executor.submit(measure_and_average, smu_address_1),
                        executor.submit(measure_and_average, smu_address_2)
                    ]
                    results = [future.result() for future in futures]
                    r1 = results[0][0]
                    r2 = results[1][0]
                meas_vol = measure_dmm(dmm_address)
                # write to Google Sheets
                row = int(arr1[j]) + i
                gsheet_util_new.write_single_value(google_sheet_id, google_sheetname, f"D{row}", meas_vol)
                gsheet_util_new.write_single_value(google_sheet_id, google_sheetname, f"H{row}", r1)
                gsheet_util_new.write_single_value(google_sheet_id, google_sheetname, f"J{row}", r2)

                # print("Minimum_voltage of 1=", min(results[0][1]))
                # print("Maximum_voltage of 1=", max(results[0][1]))
                # print("difference between min and max of 1", float(max(results[0][1]))-float(min(results[0][1])), "\n")
                # print("Minimum_voltage of 2=", min(results[1][1]))
                # print("Maximum_voltage of 2=", max(results[1][1]))
                # print("difference between min and max of 2", float(max(results[1][1]))-float(min(results[1][1])), "\n")
            
            # Final Output
            print("\n===> Final Average Voltages")
            print(f"SMU 1 Average Voltage: {results[0][0]} V")
            print(f"SMU 2 Average Voltage: {results[1][0]} V")

            time.sleep(2)
        k+=1
        
    j+=1
    gsheet_util_new.write_single_value(google_sheet_id, google_sheetname1, "B8", j)
    gsheet_util_new.write_single_value(google_sheet_id, google_sheetname1, "B9", j)


print("done")


# closng connections
gen.write("OUTPut OFF")
gen.close()
#rm.close()



    # user_input = input("Enter 'Y' to continue, 'R' to repeat current set, or anything else to exit: ").strip().lower()
    # if user_input == 'y':
    #     j += 1  # proceed to next set
    # elif user_input == 'r':
    #     print("Repeating the current set...")
    #     # j remains unchanged
    # else:
    #     print("Exiting the program.")
    #     break  # exit while loop
    # gsheet_util_new.write_single_value(google_sheet_id, google_sheetname1, "B8", j)
    # gsheet_util_new.write_single_value(google_sheet_id, google_sheetname1, "B9", j)

