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
#from data_execl_local import write_to_excel_cell

import x_y

# ===> Constants
vref = 2.5
meas_vol = 0
google_sheet_id = '1hF4Snpfwg6-8w03q6VBuWfcwUNAFX5iWZxPIyqwjrc4'
#google_sheetname2 = 'TC_G50_M1'
google_sheetname2 = 'Gain+cmrr'

#arr1 = [18, 30, 44, 58, 71, 84, 85, 97, 109, 121, 132, 144, 156, 168, 180]
arr1 = [15, 27, 36, 50, 60, 75, 87, 98, 109, 121, 132, 144, 156, 168, 180]

# CM voltage and I_sense for each iteration
cm_v = [0.5,8,8]
isense_v = [-0.005, -0.005, 0.005]
isense_vcm=[0.008,0.009,0.008]

average_window = 1

# SMU addresses for measurement
# smu_address = "USB0::0x05E6::0x2450::04495761::INSTR"
# keithley_2636b_address = 'USB0::0x05E6::0x2636::4428135::INSTR'
# function_gen_address = "USB0::0x0957::0x2807::MY58000574::INSTR"
# dmm_address_1 = "TCPIP0::K-34461A-10465.local::inst0::INSTR"
# dmm_address_2 = "USB0::0x2A8D::0x1301::MY57210468::INSTR"
# dmm_address_3 = "GPIB0::22::INSTR"

smu_address = "TCPIP::10.9.96.103::inst0::INSTR"
keithley_2636b_address = 'TCPIP0::10.9.96.113::inst0::INSTR'
function_gen_address = "TCPIP0::10.9.96.111::inst0::INSTR"
# dmm1 for vsense
dmm_address_1 = "TCPIP0::10.9.96.101::inst0::INSTR"
# dmm2 for vout
dmm_address_2 = "TCPIP0::10.9.96.105::inst0::INSTR"
# dmm3 for vcm
dmm_address_3 = "GPIB0::22::INSTR"


# ===> VISA Setup
rm = pyvisa.ResourceManager()

# function generatro setup
gen = rm.open_resource(function_gen_address)
gen.timeout = 5000


# Function to measure and average voltage from SMU
# def measure_and_average(smu_address):
#     rm = pyvisa.ResourceManager()
#     smu = rm.open_resource(smu_address)
#     smu.timeout = 5000

#     vaverage = 0.0
#     # v_all = []

#     try:
#         smu.write("*CLS")
#         smu.write("*RST")
#         smu.write(":SOUR:FUNC CURR")
#         smu.write(":SOUR:CURR 1E-9")
#         #smu.write(":SENSE:VOLT:DC:DIGITS 6.5")
#         smu.write(":SENS:FUNC 'VOLT:DC'")
#         smu.write(":SENS:VOLT:DC:NPLC 10")
#         smu.write(":OUTP ON")

#         time.sleep(2)

#         time.sleep(0.1)
#         raw_data = smu.query(":MEAS:VOLT?")
#         voltage = float(raw_data.strip())
#         print(f"Measured Voltage {i+1}: {voltage:.9f} V")
#         vaverage += voltage
#         # v_all.append(voltage)

#         err = smu.query("SYST:ERR?")
#         print("Status:", err)

#         print(f"\nAverage Voltage from smu: {vaverage:.9f} V")
#         # return vaverage, v_all
#         return vaverage

#     finally:
#         smu.write(":OUTP OFF")
#         smu.close()


# def measure_dmm (dmm_address):
#     dmm = rm.open_resource(dmm_address)
#     time.sleep(0.1)
#     dmm_v = dmm.query("MEAS:VOLT:DC?")
#     dmm.close()
#     return str(float(dmm_v))

def measure_dmm_x3 (dmm_address_1, dmm_address_2, dmm_address_3):
    dmm1 = rm.open_resource(dmm_address_1)
    dmm1.write(":SENS:VOLT:DC:NPLC 100")
    time.sleep(0.1)
    dmm2 = rm.open_resource(dmm_address_2)
    dmm2.write(":SENS:VOLT:DC:RANGE 0.1")
    dmm2.write(":SENS:VOLT:DC:NPLC 100")
    time.sleep(0.1)
    dmm3 = rm.open_resource(dmm_address_3)
    dmm3.write(":SENS:VOLT:DC:NPLC 100")
    time.sleep(0.1)

    # Measure Voltages from SMUs
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(dmm1.query, "MEAS:VOLT:DC?"),
            executor.submit(dmm2.query, "MEAS:VOLT:DC?"),
            executor.submit(dmm3.query, "MEAS:VOLT:DC?")
        ]
        results = [future.result() for future in futures]
        # r1 = str(results[0])
        # r2 = str(results[1])
        # r3 = str(results[2])
        # print(results, "these are read from the dmms")
    
    return results
    
    # dmm_v = dmm.query("MEAS:VOLT:DC?")
    # dmm.close()
    # return str(float(dmm_v))
    

t1 = time.time()

j = 0 # measurements selection (0 to 5)
google_sheetname1 = "Python_sheet"
# cell_value_pairs = [
#     ("B8", 0),
#     ("B9", 0),
#     ("B10", 0),
#     ("B11", 0),
#     ("B12", 0),
#     ("B13", 0),
#     ("B14", 0),
#     ("B15", 0),
# ]
# gsheet_util_new.write_multiple_values(google_sheet_id, google_sheetname1,cell_value_pairs)
# t2 = time.time()

# print("time to write = ", t2-t1)

t = 0.01
filename_csv = 'gsheet_trimbit_values.csv'

while j < 8:
    k = 0
    if j==0:
     cell_value_pairs = [
     ("B8", 0),
     ("B9", 0),
     ("B10", 0),
     ("B11", 0),
     ("B12", 0),
     ("B13", 0),
     ("B14", 0),
     ("B15", 0),
     ]  
     gsheet_util_new.write_multiple_values(google_sheet_id, google_sheetname1,cell_value_pairs)
#t2 = time.time()
    if j==1:
        cell_value_pairs = [
       ("B8", 1),
       ("B9", 1),
       ]
        gsheet_util_new.write_multiple_values(google_sheet_id, google_sheetname1,cell_value_pairs)
    if j==2:
        value1 = gsheet_util_new.read_single_value(google_sheet_id, google_sheetname2, "C31")
        value2 = gsheet_util_new.read_single_value(google_sheet_id, google_sheetname2, "F31")
        trim_bit1 = value1
        trim_bit2 = value2
        cell_value_pairs = [
       ("B8", value1),
       ("B9", value2),
       ]
        #print(f"Trim bits from B8: {trim_bit}")
        gsheet_util_new.write_multiple_values(google_sheet_id, google_sheetname1,cell_value_pairs)
    if j==3:
        value1 = gsheet_util_new.read_single_value(google_sheet_id, google_sheetname2, "C45")
        value2 = gsheet_util_new.read_single_value(google_sheet_id, google_sheetname2, "F48")
        trim_bit1 = value1
        trim_bit2 = 0
        #print(f"Trim bits from B8: {trim_bit}")
        cell_value_pairs = [
       ("B10", value1),
       ("B11", 0),
       ]
        gsheet_util_new.write_multiple_values(google_sheet_id, google_sheetname1, cell_value_pairs)
    if j==4:
        value1 = gsheet_util_new.read_single_value(google_sheet_id, google_sheetname2, "C45")
        value2 = gsheet_util_new.read_single_value(google_sheet_id, google_sheetname2, "C58")
        trim_bit1 = value1
        trim_bit2 = value2
        cell_value_pairs = [
       ("B10", value1),
       ("B11", value2),
       ]
        #print(f"Trim bits from B8: {trim_bit}")
        gsheet_util_new.write_multiple_values(google_sheet_id, google_sheetname1,cell_value_pairs)
    if j==5:
        value1 = gsheet_util_new.read_single_value(google_sheet_id, google_sheetname2, "C45")
        value2 = gsheet_util_new.read_single_value(google_sheet_id, google_sheetname2, "C68")
        trim_bit1 = value1
        trim_bit2 = value2
        cell_value_pairs = [
       ("B10", value1),
       ("B11", value2),
       ]
        
        #print(f"Trim bits from B8: {trim_bit}")
        gsheet_util_new.write_multiple_values(google_sheet_id, google_sheetname1, cell_value_pairs)
    if j==6:
        #value1 = gsheet_util_new.read_single_value(google_sheet_id, google_sheetname2, "C75")
        value2 = gsheet_util_new.read_single_value(google_sheet_id, google_sheetname2, "C83")
        trim_bit1 = value1
        trim_bit2 = value2
        cell_value_pairs = [
       ("B12", 0),
       ("B13", value2),
       ]
        
        #print(f"Trim bits from B8: {trim_bit}")
        gsheet_util_new.write_multiple_values(google_sheet_id, google_sheetname1, cell_value_pairs)
    if j==7:
        #value1 = gsheet_util_new.read_single_value(google_sheet_id, google_sheetname2, "C75")
        value2 = gsheet_util_new.read_single_value(google_sheet_id, google_sheetname2, "C95")
        trim_bit1 = value1
        trim_bit2 = value2
        cell_value_pairs = [
       ("B12", 0),
       ("B13", value2),
       ]
        
        #print(f"Trim bits from B8: {trim_bit}")
        gsheet_util_new.write_multiple_values(google_sheet_id, google_sheetname1, cell_value_pairs)
    if j==8:
        #value1 = gsheet_util_new.read_single_value(google_sheet_id, google_sheetname2, "C75")
        value2 = gsheet_util_new.read_single_value(google_sheet_id, google_sheetname2, "C106")
        trim_bit1 = value1
        trim_bit2 = value2
        cell_value_pairs = [
       ("B14", 0),
       ("B15", value2),
       ]
        
        #print(f"Trim bits from B8: {trim_bit}")
        gsheet_util_new.write_multiple_values(google_sheet_id, google_sheetname1, cell_value_pairs)
    

        


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
            input("unshort the inputs")
            print("Disconnecting Vsense resistor")
            relay_power_control.vsense_res_disconnect()

            print("Changing supply voltage")
           # turn_off_smu_output()
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

            time.sleep(5)


        elif k == 1:
            # Google Sheet ID and mapping of sheet names to local files
            SHEET_ID = '1hF4Snpfwg6-8w03q6VBuWfcwUNAFX5iWZxPIyqwjrc4'  # Replace with your Google Sheet ID
            
            FILE_MAP = {
                google_sheetname1: filename_csv
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
            
            if j<2:
                input('take output with 2 chips')
                r1=[]
                r2=[]
                r3=[]  # Missing colon here
                for i in range(3):
                        # if(l == 0 & i == 0):
                            # relay_power_control.vsense_res_connect()
                        relay_power_control.vsense_res_connect()
                        cm_voltage = cm_v[i]
                        
                        isense = isense_v[i]
                        isense_vcm1 = isense_vcm[i]

                        # print(f"\nIteration {i+1} - CM Voltage: {cm_voltage}, Isense: {isense}")
                        # print(j+1)

                        # --- Configure Keithley 2636B ---
                        smu = rm.open_resource(keithley_2636b_address)
                        smu_vcm = rm.open_resource(smu_address)

                        #smu_vcm.write(":OUTP ON")
                        time.sleep(0.1)

                        smu.write("smub.source.func = smub.OUTPUT_DCAMPS")
                        smu.write(f"smub.source.leveli = {isense}")
                        smu.write("smub.source.limitv = 10")
                        smu.write("smub.source.output = smub.OUTPUT_ON")

                        smu.write("smua.source.func = smua.OUTPUT_DCVOLTS")
                        smu.write(f"smua.source.levelv = {vref}")
                        smu.write("smua.source.limiti = 0.0005")
                        smu.write("smua.source.output = smub.OUTPUT_ON")
                        smu.close()
                        time.sleep(1)
                        print(f"CM voltage = {cm_voltage}")
                        smu_vcm.write(":SOUR:FUNC VOLT")
                        # time.sleep(1)
                        smu_vcm.write(f":SOUR:VOLT {cm_voltage}")
                        # time.sleep(1)
                        smu_vcm.write(":SOUR:VOLT:ILIMIT 0.01")
                        time.sleep(1)
                        #smu_vcm.write(f":SOUR:VOLT {cm_voltage}")
                        #smu_vcm.write(":SENS:CURR:PROT 0.01")
                        #:SOUR:VOLT:ILIMIT 0.01
                
                        smu_vcm.write(":SOUR:VOLT:RANG 20")
                    
                        smu_vcm.write(":OUTP ON")
                        smu_vcm.close()



                        #smu_vcm.write(":SOUR:FUNC CURR")
                        #smu_vcm.write(f":SOUR:CURR {isense_vcm1}")
                        #smu_vcm.write(":SENS:FUNC 'VOLT'")  # Measure voltage

                        time.sleep(2)

                    # Measure Voltages from SMUs
                        results = measure_dmm_x3(dmm_address_1, dmm_address_2, dmm_address_3)
                        # r1 = str(float(results[0]))
                        # r2 = str(float(results[1]))
                        # r3 = str(float(results[2]))
                        #row = int(arr1[j]) + i
                        r1.append(float(results[0]))
                        r2.append(float(results[1]))
                        r3.append(float(results[2]))
                        # cell_value_pairs = [
                        # (f"D{row}", r3),
                        # (f"H{row}", r1),
                        # (f"J{row}", r2)
                        # ]
                        # print("r1 is", r1)
                        # print("r2 is", r2)
                        # print("r3 is", r3)
                        
                # gain_x_gain_y.compute_gain_xy(r3, r2,r1)
                print(r1,r2,r3)
                print("Execution at line ", )
                gainx, gainy = x_y.compute_x_y(r1, r2, r3)
                print(gainx,gainy)
                
                row = int(arr1[j])
                print(row,j, k)
                cell_value_pairs = [
                    (f"C{row}", gainx),
                    (f"C{row+1}", gainy),
                    ]
                gsheet_util_new.write_multiple_values(google_sheet_id, google_sheetname2,cell_value_pairs)

                
            time.sleep(2)
            if j==2:
                r1=[]
                r2=[]
                r3=[]
                input("switching to 2 set measurement,check output with 2 chips")
                for i in range(2):
                    
                    relay_power_control.vsense_res_connect()
                    cm_voltage = 0.5
                    isense_v2=[-0.005,0.005]
                    isense = isense_v2
                    isense_vcm1 = isense_vcm[i]

                    # print(f"\nIteration {i+1} - CM Voltage: {cm_voltage}, Isense: {isense}")
                    # print(j+1)

                    # --- Configure Keithley 2636B ---
                    smu = rm.open_resource(keithley_2636b_address)
                    smu_vcm = rm.open_resource(smu_address)

                    #smu_vcm.write(":OUTP ON")
                    time.sleep(0.1)

                    smu.write("smub.source.func = smub.OUTPUT_DCAMPS")
                    smu.write(f"smub.source.leveli = {isense[i]}")
                    smu.write("smub.source.limitv = 10")
                    smu.write("smub.source.output = smub.OUTPUT_ON")

                    smu.write("smua.source.func = smua.OUTPUT_DCVOLTS")
                    smu.write(f"smua.source.levelv = {vref}")
                    smu.write("smua.source.limiti = 0.0005")
                    smu.write("smua.source.output = smub.OUTPUT_ON")
                    smu.close()
                    time.sleep(1)
                    print(f"CM voltage = {cm_voltage}")
                    smu_vcm.write(":SOUR:FUNC VOLT")
                    # time.sleep(1)
                    smu_vcm.write(f":SOUR:VOLT {cm_voltage}")
                    # time.sleep(1)
                    smu_vcm.write(":SOUR:VOLT:ILIMIT 0.01")
                    time.sleep(1)
                    #smu_vcm.write(f":SOUR:VOLT {cm_voltage}")
                    #smu_vcm.write(":SENS:CURR:PROT 0.01")
                    #:SOUR:VOLT:ILIMIT 0.01
            
                    smu_vcm.write(":SOUR:VOLT:RANG 20")
                
                    smu_vcm.write(":OUTP ON")
                    smu_vcm.close()



                    #smu_vcm.write(":SOUR:FUNC CURR")
                    #smu_vcm.write(f":SOUR:CURR {isense_vcm1}")
                    #smu_vcm.write(":SENS:FUNC 'VOLT'")  # Measure voltage

                    time.sleep(2)

                # Measure Voltages from SMUs
                    results = measure_dmm_x3(dmm_address_1, dmm_address_2, dmm_address_3)
                    # r1 = str(float(results[0]))
                    # r2 = str(float(results[1]))
                    # r3 = str(float(results[2]))
                    #row = int(arr1[j]) + i
                    r1.append(float(results[0]))
                    r2.append(float(results[1]))
                    r3.append(float(results[2]))
                    print(r1,r2,r3)
                    #r1= vsense,r2=vout,r3=vcm
                    print("Execution at line ", )
                    #gainx, gainy = x_y.compute_x_y(r1, r2, r3)
                    #print(gainx,gainy)
                
                    row = int(arr1[j])
                    print(row,j, k)
                    cell_value_pairs = [
                    (f"D{row+i}", r2[i]),
                    (f"G{row+i}", r1[i]),
                    ]
                    gsheet_util_new.write_multiple_values(google_sheet_id, google_sheetname2,cell_value_pairs)
            if j>2:
                r1=[]
                r2=[]
                r3=[]
                input("switching to cmrr measurement,Short the two inputs")
                for i in range(2):
                    
                    relay_power_control.vsense_res_connect()
                    cm_voltage = [0.5,20]
                    
                    isense = 0
                    isense_vcm1 = isense_vcm[i]

                    # print(f"\nIteration {i+1} - CM Voltage: {cm_voltage}, Isense: {isense}")
                    # print(j+1)

                    # --- Configure Keithley 2636B ---
                    smu = rm.open_resource(keithley_2636b_address)
                    smu_vcm = rm.open_resource(smu_address)

                    #smu_vcm.write(":OUTP ON")
                    time.sleep(0.1)

                    smu.write("smub.source.func = smub.OUTPUT_DCAMPS")
                    smu.write(f"smub.source.leveli = {isense}")
                    smu.write("smub.source.limitv = 10")
                    smu.write("smub.source.output = smub.OUTPUT_ON")

                    smu.write("smua.source.func = smua.OUTPUT_DCVOLTS")
                    smu.write(f"smua.source.levelv = {vref}")
                    smu.write("smua.source.limiti = 0.0005")
                    smu.write("smua.source.output = smub.OUTPUT_ON")
                    smu.close()
                    time.sleep(1)
                    print(f"CM voltage = {cm_voltage[i]}")
                    smu_vcm.write(":SOUR:FUNC VOLT")
                    # time.sleep(1)
                    smu_vcm.write(f":SOUR:VOLT {cm_voltage[i]}")
                    # time.sleep(1)
                    smu_vcm.write(":SOUR:VOLT:ILIMIT 0.01")
                    time.sleep(1)
                    #smu_vcm.write(f":SOUR:VOLT {cm_voltage}")
                    #smu_vcm.write(":SENS:CURR:PROT 0.01")
                    #:SOUR:VOLT:ILIMIT 0.01
            
                    smu_vcm.write(":SOUR:VOLT:RANG 20")
                
                    smu_vcm.write(":OUTP ON")
                    smu_vcm.close()



                    #smu_vcm.write(":SOUR:FUNC CURR")
                    #smu_vcm.write(f":SOUR:CURR {isense_vcm1}")
                    #smu_vcm.write(":SENS:FUNC 'VOLT'")  # Measure voltage

                    time.sleep(10)

                # Measure Voltages from SMUs
                    results = measure_dmm_x3(dmm_address_1, dmm_address_2, dmm_address_3)
                    # r1 = str(float(results[0]))
                    # r2 = str(float(results[1]))
                    # r3 = str(float(results[2]))
                    #row = int(arr1[j]) + i
                    r1.append(float(results[0]))
                    r2.append(float(results[1]))
                    r3.append(float(results[2]))
                    print(r1,r2,r3)
                    #r1= vsense,r2=vout,r3=vcm
                    print("Execution at line ", )
                    #gainx, gainy = x_y.compute_x_y(r1, r2, r3)
                    #print(gainx,gainy)
                
                    row = int(arr1[j])
                    #print(row,j, k)
                    cell_value_pairs = [
                    (f"D{row+i}", r2[i]),
                    (f"G{row+i}", r3[i]),
                    (f"J{row+i}",r1[i])
                    ]
                    gsheet_util_new.write_multiple_values(google_sheet_id, google_sheetname2,cell_value_pairs)


        k += 1

    j += 1
           

print("done")


# closng connections
gen.write("OUTPut OFF")
gen.close()
