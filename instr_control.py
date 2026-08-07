import pyvisa
import time
from constants import dmm1_addr, dmm2_addr, dmm3_addr, smu_2ch_addr, smu_bad_addr, psu_addr, afg_addr, res_connection_delay, SMUchA_current_limit, SMUchB_voltage_limit
from concurrent.futures import ThreadPoolExecutor
rm = pyvisa.ResourceManager()

def SMUchA_voltage_set(voltage):
    smu = rm.open_resource(smu_2ch_addr)
    time.sleep(0.1)
    smu.write("smua.source.func = smua.OUTPUT_DCVOLTS")
    smu.write(f"smua.source.levelv = {voltage}")
    smu.write(f"smua.source.limiti = {SMUchA_current_limit}")
    smu.write("smua.source.output = smua.OUTPUT_ON")
    smu.close()
    time.sleep(1)

def SMUchB_current_set(current):
    smu = rm.open_resource(smu_2ch_addr)
    time.sleep(0.1)
    smu.write("smub.source.func = smub.OUTPUT_DCAMPS")
    smu.write(f"smub.source.leveli = {current}")
    smu.write(f"smub.source.limitv = {SMUchB_voltage_limit}")
    smu.write("smub.source.output = smub.OUTPUT_ON")
    smu.close()
    time.sleep(1)

def SMUbad_voltage_set(voltage):
    # Write code here
    smu_vcm = rm.open_resource(smu_bad_addr)
    # time.sleep(1)
    smu_vcm.write(":SOUR:FUNC VOLT")
    smu_vcm.write(":SOUR:VOLT:RANG 200")
    smu_vcm.write(":SENS:CURR:RANG 0.001")
    smu_vcm.write(":SOUR:VOLT:ILIMIT 0.001")
    smu_vcm.write(":SENS:CURR:RANG 0.001")
    # time.sleep(1)
    smu_vcm.write(f":SOUR:VOLT {voltage}")
    smu_vcm.write(":OUTP ON")
    time.sleep(1)
    smu_vcm.query(":MEAS:CURR?")
    smu_vcm.close()

def SMU_shutdown():
    smu_vcm = rm.open_resource(smu_bad_addr)
    smu = rm.open_resource(smu_2ch_addr)
    
    smu_vcm.write(":OUTP OFF")
    smu.write("smua.source.output = smua.OUTPUT_OFF")
    smu.write("smub.source.output = smub.OUTPUT_OFF")
    time.sleep(1)
    smu_vcm.close()
    smu.close()
    

def dmm_measure_x3_setup():
    dmm1 = rm.open_resource(dmm1_addr)
    dmm1.write(":SENS:VOLT:DC:RANGE 0.1")
    dmm1.write(":SENS:VOLT:DC:NPLC 100")
    dmm1.write("TRIG:SOUR BUS")
    # dmm1.write("INIT\n")
    # time.sleep(0.1)
    dmm2 = rm.open_resource(dmm2_addr)
    dmm2.write(":SENS:VOLT:DC:RANGE 1")
    dmm2.write(":SENS:VOLT:DC:NPLC 100")
    dmm2.write("TRIG:SOUR BUS")
    # dmm2.write("INIT\n")
    # time.sleep(0.1)
    dmm3 = rm.open_resource(dmm3_addr)
    dmm3.write(":SENS:VOLT:DC:RANGE 100")
    dmm3.write(":SENS:VOLT:DC:NPLC 100")
    dmm3.write("TRIG:SOUR BUS")
    # dmm3.write("INIT\n")
    # time.sleep(0.1)

    # # Trigger Voltages from SMUs - concurrency is required. storing their results is not required
    # with ThreadPoolExecutor() as executor:
    #     futures = [
    #         executor.submit(dmm1.write, "*TRG\n"),
    #         executor.submit(dmm2.write, "*TRG\n"),
    #         executor.submit(dmm3.write, "*TRG\n")
    #     ]
    #     results = [float(future.result()) for future in futures]

    # time.sleep(4)

    # # Measure Voltages from SMUs - concurrency is not required
    # with ThreadPoolExecutor() as executor:
    #     futures = [
    #         executor.submit(dmm1.query, "FETCH?"),
    #         executor.submit(dmm2.query, "FETCH?"),
    #         executor.submit(dmm3.query, "FETCH?")
    #     ]
    #     results = [float(future.result()) for future in futures]


    # dmm1.close()
    # dmm2.close()
    # dmm3.close()

    # return results
    return dmm1, dmm2, dmm3

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
    # This should be 2 seconds + some small delay, but it realistically takes 4 seconds, or it bugs out during fetch
    time.sleep(4)

    r11 = float(dmm1.query("FETCH?"))
    r21 = float(dmm2.query("FETCH?"))
    r31 = float(dmm3.query("FETCH?"))

    # return results
    return r11, r21, r31

def dmm_measure_x3_deinit(dmm1, dmm2, dmm3):
    dmm1.close()
    dmm2.close()
    dmm3.close()

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

def VSUP_voltage_set(voltage, current_limit):
    psu = rm.open_resource(psu_addr)
    psu.write("INST:NSEL 1")
    psu.write(f"VOLT {voltage}")
    psu.write(f"CURR {current_limit}")
    psu.write("OUTP ON")  # Turn on output for the channel
    psu.close()

def vsense_res_disconnect():
    # --- Define settings for each channel ---
    channel_settings = {
        1: {'voltage': 0, 'current': 0.20},
        2: {'voltage': 5, 'current': 0.20},
        3: {'voltage': 5, 'current': 0.20}
    }

    psu = rm.open_resource(psu_addr)

    # Apply settings to each channel
    for channel, settings in channel_settings.items():
        voltage = settings['voltage']
        current = settings['current']
        
        psu.write(f"INST:NSEL {channel}")
        psu.write(f"VOLT {voltage}")
        psu.write(f"CURR {current}")
        psu.write("OUTP ON")  # Turn on output for the channel

        # print(f"Channel {channel} set to {voltage} V, {current} A")

    time.sleep(res_connection_delay)

    psu.close()

def vsense_res_connect():
    # --- Define settings for each channel ---
    channel_settings = {
        1: {'voltage': 5, 'current': 0.2},
        2: {'voltage': 0, 'current': 0.2},  # Use parameter here
        3: {'voltage': 5, 'current': 0.2}
    }

    psu = rm.open_resource(psu_addr)
    # print("Connected to:", psu.query("*IDN?").strip())

    # Apply settings to each channel
    for channel, settings in channel_settings.items():
        voltage = settings['voltage']
        current = settings['current']
        
        psu.write(f"INST:NSEL {channel}")
        psu.write(f"VOLT {voltage}")
        psu.write(f"CURR {current}")
        psu.write("OUTP ON")

        # print(f"Channel {channel} set to {voltage} V, {current} A")

    time.sleep(res_connection_delay)  # Delay to stabilize output

    psu.close()

def SMUchA_output_off():
    # Connect to the Keithley 2636B using the correct VISA address
    smu = rm.open_resource(smu_2ch_addr)  # Replace with your actual VISA address

    # Verify connection (optional)
    # print("Connected to:", smu.query("*IDN?").strip())

    smu.write("smua.source.output = smua.OUTPUT_OFF")       # Enable output
    
    smu.close()

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