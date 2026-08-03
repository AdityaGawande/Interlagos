import pyvisa
import time
from concurrent.futures import ThreadPoolExecutor
import gsheet_util_new  # Assumes you have this utility

# ===> Constants
vref = 2.5
meas_vol = 0
google_sheet_id = '1hF4Snpfwg6-8w03q6VBuWfcwUNAFX5iWZxPIyqwjrc4'
google_sheetname = 'TC_G50'
arr1 = [13, 25, 39, 53, 66, 79]

# CM voltage and I_sense for each iteration
cm_v = [0.5, 0.6, 0.5]
isense_v = [0.002, 0.002, 0.004]

# SMU addresses for measurement
smu_address_1 = "USB0::0x05E6::0x2450::04495761::INSTR"
smu_address_2 = "USB0::0x05E6::0x2460::04323817::INSTR"
keithley_2636b_address = 'USB0::0x05E6::0x2636::4428135::INSTR'
function_gen_address = "USB0::0x0957::0x5707::MY53804311::INSTR"
dmm_address = "USB0::0x2A8D::0x1301::MY57210465::INSTR"


# ===> VISA Setup
rm = pyvisa.ResourceManager()

# function generatro setup
gen = rm.open_resource(function_gen_address)
gen.timeout = 5000

# Function to measure and average voltage from SMU
def measure_and_average(smu_address, num_measurements=100):
    smu = rm.open_resource(smu_address)
    smu.timeout = 5000
    smu.write("OUTP ON")
    vaverage = 0.0
    v_all = []
    for i in range(num_measurements):
        voltage_str = smu.query("MEAS:VOLT?")
        voltage = float(voltage_str)
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
for i in range(3):
    cm_voltage = cm_v[i]
    isense = isense_v[i]

    print(f"\n=== Iteration {i+1} - CM Voltage: {cm_voltage}, Isense: {isense} ===")

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
    time.sleep(1)

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

    print("Minimum_voltage of 1=", min(results[0][1]))
    print("Maximum_voltage of 1=", max(results[0][1]))
    print("difference between min and max of 1", float(max(results[0][1]))-float(min(results[0][1])), "\n")
    print("Minimum_voltage of 2=", min(results[1][1]))
    print("Maximum_voltage of 2=", max(results[1][1]))
    print("difference between min and max of 2", float(max(results[1][1]))-float(min(results[1][1])), "\n")
    

# Final Output
print("\n===> Final Average Voltages")
print(f"SMU 1 Average Voltage: {results[0][0]} V")
print(f"SMU 2 Average Voltage: {results[1][0]} V")

# closng connections
gen.write("OUTPut OFF")
gen.close()
rm.close()
