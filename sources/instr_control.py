import time
from sources.constants import *
from concurrent.futures import ThreadPoolExecutor

# rm = pyvisa.ResourceManager()
import sources.pyvisa_error_handle as rm

delay1 = sleep_after_resource_open
delay2 = sleep_after_voltage_change

# Easy to read wrappers
def VREF_set(voltage):
    SMUbad_voltage_set(voltage)

def VREF_off():
    SMUbad_shutdown()
    
def VCM_set(voltage):
    SMUchA_voltage_set(voltage)

def Isense_set(current):
    SMUchB_current_set(current)

## SMU section
def SMUchA_voltage_set(voltage):
    smu = rm.open_resource(smu_2ch_addr)
    time.sleep(delay1)
    smu.write("smua.source.func = smua.OUTPUT_DCVOLTS")
    smu.write(f"smua.source.rangev = {SMUchA_voltage_range}")
    smu.write(f"smua.source.levelv = {voltage}")
    smu.write(f"smua.source.limiti = {SMUchA_current_limit}")
    smu.write("smua.source.output = smua.OUTPUT_ON")
    smu.close()
    time.sleep(delay2)

def SMUchB_current_set(current):
    smu = rm.open_resource(smu_2ch_addr)
    time.sleep(delay1)
    smu.write("smub.source.func = smub.OUTPUT_DCAMPS")
    smu.write(f"smub.source.leveli = {current}")
    smu.write(f"smub.source.limitv = {SMUchB_voltage_limit}")
    smu.write("smub.source.output = smub.OUTPUT_ON")
    smu.close()
    time.sleep(delay2)

def SMUbad_voltage_set(voltage):
    smu_vcm = rm.open_resource(smu_bad_addr)
    # time.sleep(1)
    smu_vcm.write(":SOUR:FUNC VOLT")
    smu_vcm.write(f":SOUR:VOLT:RANG {SMUbad_voltage_range}")
    smu_vcm.write(f":SENS:CURR:RANG {SMUbad_current_range}")
    smu_vcm.write(f":SOUR:VOLT:ILIMIT {SMUbad_current_limit}")
    smu_vcm.write(f":SENS:CURR:RANG {SMUbad_current_limit}") 
    # This is because the SMU does not allow massive jumps in either 
    # sense range or source limit (they are related)
    # time.sleep(1)
    smu_vcm.write(f":SOUR:VOLT {voltage}")
    smu_vcm.write(":OUTP ON")
    
    time.sleep(delay2)
    # If current is not measured, the SMU sometimes gets stuck with an old isense measurement.
    # The old isense measurement may hit the limit, and the output voltage is not correct.
    smu_vcm.query(":MEAS:CURR?")
    
    smu_vcm.close()

# SMU shutdown (Turns outputs off)
def SMU_shutdown():
    smu_vcm = rm.open_resource(smu_bad_addr)
    smu = rm.open_resource(smu_2ch_addr)
    smu_vcm.write(":OUTP OFF")
    smu.write("smua.source.output = smua.OUTPUT_OFF")
    smu.write("smub.source.output = smub.OUTPUT_OFF")
    time.sleep(delay2)
    smu_vcm.close()
    smu.close()

def SMUbad_shutdown():
    smu_vcm = rm.open_resource(smu_bad_addr)
    # smu = rm.open_resource(smu_2ch_addr)
    
    smu_vcm.write(":OUTP OFF")
    # smu.write("smua.source.output = smua.OUTPUT_OFF")
    # smu.write("smub.source.output = smub.OUTPUT_OFF")
    # time.sleep(1)
    smu_vcm.close()
    # smu.close()

def SMUchA_output_off():
    smu = rm.open_resource(smu_2ch_addr)
    smu.write("smua.source.output = smua.OUTPUT_OFF")
    smu.close()

## AFG section
# Sets a DC voltage on AFG ch1 for IREF measurement
def CLK_DC_voltage_set(voltage):
    afg = rm.open_resource(afg_addr)
    afg.write("SOUR1:BURST:STATE OFF")
    afg.write("OUTP1 OFF")
    afg.write("SOUR1:FUNC DC")
    afg.write(f"OUTP1:LOAD {afg_load_res}")
    afg.write(f"SOUR1:VOLT:OFFS {voltage}")
    afg.write("OUTP1 ON")

## DMM measurements section - Trimming mode
# Measures CLK on DMM2. Assumes clock is already visible at DMM2. Returns freq in KHz
def dmm_measure_clk(report=1):
    dmm2 = rm.open_resource(dmm2_addr)
    dmm2.write("CONF:FREQ")
    dmm2.write("FREQ:VOLT:RANG 1")
    dmm2.write("FREQ:RANG:LOW 200")
    dmm2.write("FREQ:APER 0.01")
    dmm2.write("TRIG:SOUR BUS")
    dmm2.write("INIT")
    # time.sleep(0.5)
    dmm2.write("*TRG")
    # time.sleep(1.5)
    frequency = float(dmm2.query("FETCH?"))/1000
    if(report == 1):
        print(f"Frequency in testmode is {frequency:.3f}KHz")
    dmm2.close()
    return frequency*1000

# Measures VBG on DMM2. Assumes voltage is already visible at DMM2. Returns voltage in V
def dmm_measure_vbg(report=1):
    dmm2 = rm.open_resource(dmm2_addr)
    dmm2.write("CONF:VOLT")
    dmm2.write(":SENS:VOLT:DC:RANGE 10")
    dmm2.write(":SENS:VOLT:DC:NPLC 1")
    dmm2.write("TRIG:SOUR BUS")
    dmm2.write("INIT")
    # time.sleep(0.5)
    dmm2.write("*TRG")
    # time.sleep(1.5)
    voltage = float(dmm2.query("FETCH?"))
    if(report == 1):
        print(f"Bandgap Voltage in testmode is {voltage:.6f}V")
    dmm2.close()
    return voltage

# Measures Iq on DMM3. Returns current in A
def dmm_measure_iq():
    dmm3 = rm.open_resource(dmm3_addr)
    dmm3.write("CONF:CURR")
    dmm3.write(":SENS:CURR:DC:RANGE 0.001")
    dmm3.write(":SENS:CURR:DC:NPLC 1")
    dmm3.write("TRIG:SOUR BUS")
    dmm3.write("INIT")
    # time.sleep(0.5)
    dmm3.write("*TRG")
    # time.sleep(1.5)
    current = float(dmm3.query("FETCH?"))
    # print(f"Supply current is {current*10^6}uA")
    dmm3.close()
    return current

# Measures Iref on DMM1. Assumes current is already visible at DMM1. Returns current in A
def dmm_measure_iref(report=1):
    dmm1 = rm.open_resource(dmm1_addr)
    dmm1.write("CONF:CURR")
    dmm1.write(":SENS:CURR:DC:RANGE 0.0001")
    dmm1.write(":SENS:CURR:DC:NPLC 1")
    dmm1.write("TRIG:SOUR BUS")
    dmm1.write("INIT")
    # time.sleep(0.5)
    dmm1.write("*TRG")
    # time.sleep(2)
    current = float(dmm1.query("FETCH?"))
    if(report == 1):
        print(f"IREF current is {(current*(float(1000000000))):.0f}nA")
    # print(f"Supply current is {current*10^6}uA")
    dmm1.close()
    return current

# Wrappers for printing current into terminal
def Testmode_current_check():
    current = dmm_measure_iq()
    print(f"Supply current in testmode is {(current*(float(1000000))):.2f}uA")

def Amplifier_current_check():
    current = dmm_measure_iq()
    print(f"Supply current in amplifier mode is {(current*(float(1000000))):.2f}uA")


## DMM measurements section - Amplifier mode
# Provides handles for the DMMs. Sets up NPLC, range and Trigger mode
def dmm_measure_x3_setup():
    dmm1 = rm.open_resource(dmm1_addr)
    dmm1.write(":SENS:VOLT:DC:RANGE 0.1")
    dmm1.write(":SENS:VOLT:DC:NPLC 100")
    dmm1.write("TRIG:SOUR BUS")

    dmm2 = rm.open_resource(dmm2_addr)
    dmm2.write(":SENS:VOLT:DC:RANGE 1")
    dmm2.write(":SENS:VOLT:DC:NPLC 100")
    dmm2.write("TRIG:SOUR BUS")

    dmm3 = rm.open_resource(dmm3_addr)
    dmm3.write(":SENS:VOLT:DC:RANGE 100")
    dmm3.write(":SENS:VOLT:DC:NPLC 100")
    dmm3.write("TRIG:SOUR BUS")

    return dmm1, dmm2, dmm3

# Three measurements taken simultaneously. Returns the results as float
def dmm_measure_x3_single(dmm1, dmm2, dmm3):   
    # Sent at the same time to ensure the delays to the trigger command are same
    # Tried this for debugging higher timings while measuring 1V and 100V, but kept for the principle of it
    with ThreadPoolExecutor() as executor:
        executor.submit(dmm1.write, "INIT\n")
        executor.submit(dmm2.write, "INIT\n")
        executor.submit(dmm3.write, "INIT\n")

    # Trigger Voltages from SMUs - concurrency is required. storing their results is not required
    with ThreadPoolExecutor() as executor:
        executor.submit(dmm1.write, "*TRG\n")
        executor.submit(dmm2.write, "*TRG\n")
        executor.submit(dmm3.write, "*TRG\n")
    # This should be 2 seconds + some small delay, but it realistically takes 4 seconds, 
    # or it bugs out during fetch
    time.sleep(4)

    r11 = float(dmm1.query("FETCH?"))
    r21 = float(dmm2.query("FETCH?"))
    r31 = float(dmm3.query("FETCH?"))

    # return results
    return r11, r21, r31

# Closes DMM handles
def dmm_measure_x3_deinit(dmm1, dmm2, dmm3):
    dmm1.close()
    dmm2.close()
    dmm3.close()

# Deprecated
def dmm_measure_x3():
    # Deprecated. Do not use. Although it should still work
    dmm1 = rm.open_resource(dmm1_addr)
    dmm1.write(":SENS:VOLT:DC:RANGE 0.1")
    dmm1.write(":SENS:VOLT:DC:NPLC 100")
    dmm1.write("TRIG:SOUR BUS")
    dmm1.write("INIT\n")
    time.sleep(0.1)
    dmm2 = rm.open_resource(dmm2_addr)
    dmm2.write(":SENS:VOLT:DC:RANGE 1")
    dmm2.write(":SENS:VOLT:DC:NPLC 100")
    dmm2.write("TRIG:SOUR BUS")
    dmm2.write("INIT\n")
    time.sleep(0.1)
    dmm3 = rm.open_resource(dmm3_addr)
    dmm3.write(":SENS:VOLT:DC:RANGE 100")
    dmm3.write(":SENS:VOLT:DC:NPLC 100")
    dmm3.write("TRIG:SOUR BUS")
    dmm3.write("INIT\n")
    time.sleep(0.1)

    # Trigger Voltages from SMUs - concurrency is required. storing their results is not required
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(dmm1.write, "*TRG\n"),
            executor.submit(dmm2.write, "*TRG\n"),
            executor.submit(dmm3.write, "*TRG\n")
        ]
        results = [float(future.result()) for future in futures]

    time.sleep(4)

    # Measure Voltages from SMUs - concurrency is not required
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(dmm1.query, "FETCH?"),
            executor.submit(dmm2.query, "FETCH?"),
            executor.submit(dmm3.query, "FETCH?")
        ]
        results = [float(future.result()) for future in futures]


    dmm1.close()
    dmm2.close()
    dmm3.close()

    return results

## PSU commands section
# Sets supply voltage for one CSA
def VSUP_voltage_set(IC_num, voltage):
    psu = rm.open_resource(psu_addr)
    psu.write(f"INST:NSEL {IC_num}")
    psu.write(f"VOLT {voltage}")
    psu.write(f"CURR {VSUP_current_limit}")
    psu.write("OUTP ON")  # Turn on output for the channel
    psu.close()

# Turns the supply off and on - to ensure testmode is exited
def VSUP_voltage_reset(IC_num):
    psu = rm.open_resource(psu_addr)
    psu.write(f"INST:NSEL {IC_num}")
    psu.write("OUTP OFF")  # Turn on output for the channel
    time.sleep(0.3)
    psu.write("OUTP ON")  # Turn on output for the channel
    psu.close()   

# Changes relay supply voltage for trim circuit config
def circuit_config_trim():
    psu = rm.open_resource(psu_addr)
    psu.write(f"INST:NSEL 3")
    psu.write(f"VOLT 5")
    psu.write(f"CURR {relay_current_limit}")
    psu.write("OUTP ON")  # Turn on output for the channel
    time.sleep(res_connection_delay)
    psu.close() 

# Changes relay supply voltage for amplifier circuit config
def circuit_config_amp():
    psu = rm.open_resource(psu_addr)
    psu.write(f"INST:NSEL 3")
    psu.write(f"VOLT 0")
    psu.write(f"CURR {relay_current_limit}")
    psu.write("OUTP ON")  # Turn on output for the channel
    time.sleep(res_connection_delay)
    psu.close() 


## Sanity checks
def instrument_check():
    dmm1 = rm.open_resource(dmm1_addr)
    print("Connected to:", dmm1.query("*IDN?").strip())
    dmm1.close()

    dmm2 = rm.open_resource(dmm2_addr)
    print("Connected to:", dmm2.query("*IDN?").strip())
    dmm2.close()

    dmm3 = rm.open_resource(dmm3_addr)
    print("Connected to:", dmm3.query("*IDN?").strip())
    dmm3.close()

    smu = rm.open_resource(smu_2ch_addr)
    print("Connected to:", smu.query("*IDN?").strip())
    smu.close()

    smu_bad = rm.open_resource(smu_bad_addr)
    print("Connected to:", smu_bad.query("*IDN?").strip())
    smu_bad.close()

    afg = rm.open_resource(afg_addr)
    print("Connected to:", afg.query("*IDN?").strip())
    afg.close()
    
    psu = rm.open_resource(psu_addr)
    print("Connected to:", psu.query("*IDN?").strip())
    psu.close()

# Res connect and disconnect are deprecated
# def vsense_res_disconnect():
#     # --- Define settings for each channel ---
#     channel_settings = {
#         1: {'voltage': 0, 'current': 0.20},
#         2: {'voltage': 5, 'current': 0.20},
#         3: {'voltage': 5, 'current': 0.20}
#     }

#     psu = rm.open_resource(psu_addr)

#     # Apply settings to each channel
#     for channel, settings in channel_settings.items():
#         voltage = settings['voltage']
#         current = settings['current']
        
#         psu.write(f"INST:NSEL {channel}")
#         psu.write(f"VOLT {voltage}")
#         psu.write(f"CURR {current}")
#         psu.write("OUTP ON")  # Turn on output for the channel

#         # print(f"Channel {channel} set to {voltage} V, {current} A")

#     time.sleep(res_connection_delay)

#     psu.close()

# Res connect and disconnect are deprecated
# def vsense_res_connect():
#     # --- Define settings for each channel ---
#     channel_settings = {
#         1: {'voltage': 5, 'current': 0.2},
#         2: {'voltage': 0, 'current': 0.2},  # Use parameter here
#         3: {'voltage': 5, 'current': 0.2}
#     }

#     psu = rm.open_resource(psu_addr)
#     # print("Connected to:", psu.query("*IDN?").strip())

#     # Apply settings to each channel
#     for channel, settings in channel_settings.items():
#         voltage = settings['voltage']
#         current = settings['current']
        
#         psu.write(f"INST:NSEL {channel}")
#         psu.write(f"VOLT {voltage}")
#         psu.write(f"CURR {current}")
#         psu.write("OUTP ON")

#         # print(f"Channel {channel} set to {voltage} V, {current} A")

#     time.sleep(res_connection_delay)  # Delay to stabilize output

#     psu.close()



