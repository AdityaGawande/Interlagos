import time
import x_y
import relay_power_control
from concurrent.futures import ThreadPoolExecutor
import pyvisa

from constants import smu_2ch_addr, smu_bad_addr

function_gen_address = "TCPIP0::10.9.96.111::inst0::INSTR"
# dmm1 for vsense
dmm_address_1 = "TCPIP0::10.9.96.101::inst0::INSTR"
# dmm2 for vout
dmm_address_2 = "TCPIP0::10.9.96.105::inst0::INSTR"
# dmm3 for vcm
dmm_address_3 = "GPIB0::22::INSTR"

cm_v = [0.5,8,8]
isense_v = [-0.005, -0.005, 0.005]
isense_vcm=[0.008,0.009,0.008]
vref = 2.5

rm = pyvisa.ResourceManager()

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
 

def combined_measurement():
    
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
        smu = rm.open_resource(smu_2ch_addr)
        smu_vcm = rm.open_resource(smu_bad_addr)

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

    return gainx, gainy