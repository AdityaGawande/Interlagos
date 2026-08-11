import pyvisa
import time
from constants import smu_2ch_addr, afg_addr, afg_load_res, SMUchA_voltage_range

# Low and high level of the data and clock in volts
low_level = 0.005
high_level = 2.5

t = 0.05
def run_clk_sequence(t):
    
    rm = pyvisa.ResourceManager()
    # smu = rm.open_resource("UUSB0::0x0957::0x2807::MY58000574::INSTR")
    # #smu.write("*RST")
    # smu.write("OUTP1 OFF")
    # smu.write("OUTP1:LOAD 68")  # Set the load impedance to infinity
    # smu.write("SOUR1:FREQ 5")  # Set the pulse frequency to 100 Hz
    # smu.write("SOUR1:VOLT 2.50")  # Set the pulse peak-to-peak voltage to 5 V
    # smu.write("SOUR1:VOLT:OFFS 1.25")  # Set the voltage offset to 2.5 V (0-5 V swing)
    # #smu.write("SOUR1:PULSE:DUTY 90")  # Set the duty cycle to 50%
    # smu.write("SOUR1:FUNC PULSE")  # Set the source function to pulse
    # smu.write("SOURCE1:FUNC:PULS:WIDT 100 ms\n")
    # smu.write("SOUR1:BURST:STATE ON")  # Enable burst mode
    # smu.write("SOUR1:BURST:MODE TRIGGERED")  # Set burst mode to triggered
    # smu.write("TRIG:SOURCE INT")
    # smu.write("TRIG:INT:PER 0.3")  # Set burst period to 1 second
    
    
    
    
    # print(rm)
    # print(rm.list_resources())
    # smu = rm.open_resource("USB0::0x0957::0x5707::MY53804311::INSTR")
    # #smu.write("*RST")
    # smu.write("OUTP1 OFF")

    # smu.write("SOUR1:FREQ 5")  # Set the pulse frequency to 100 Hz
    # smu.write("SOUR1:VOLT 2.50")  # Set the pulse peak-to-peak voltage to 5 V
    # smu.write("SOUR1:VOLT:OFFS 1.25")  # Set the voltage offset to 2.5 V (0-5 V swing)
    # #smu.write("SOUR1:PULSE:DUTY 90")  # Set the duty cycle to 50%
    # smu.write("SOUR1:FUNC PULSE")  # Set the source function to pulse
    # smu.write("SOURCE1:FUNC:PULS:WIDT 100 ms\n")
    # # smu.write("SOUR1:VOLT 3.3")  # Set the pulse peak-to-peak voltage to 5 V
    # # smu.write("SOUR1:VOLT:OFFS 1.65")  # Set the voltage offset to 2.5 V (0-5 V swing)
    # smu.write("OUTP1:LOAD 68")  # Set the load impedance to infinity

    

    # smu.write("SOUR1:BURST:MODE TRIGGERED")  # Set burst mode to triggered
    # smu.write("SOUR1:BURST:NCYCLES 1")  # Set number of cycles per trigger to 1
    # smu.write("SOUR1:BURST:STATE ON")  # Enable burst mode
    # #smu.write("SOUR1:BURST:INT:PER 0.205")  # Set burst period to 0.205 second
    # smu.write("OUTP1 ON")
    # smu.write("OUTP1:TRIG:SLOPE POSITIVE")  # Set trigger slope to positive
    
    # smu.write("TRIG1:SOUR BUS")  # Set the trigger source to BUS
    #smu.write("SOUR1:BURST:INT:PER 0.205")  # Set burst period to 0.205 second
    # smu.write("SOUR1:BURST:INT:PER 1")  # Set burst period to 1 second
    

    
    # smu.write("SOURCE1:TRIG:SOUR BUS")
    
    #smu.write("*TRG \n")
    

def run_smu_sequence_legacy(length, arr_high, arr_low, t=0.00025):
    if len(arr_high) != length or len(arr_low) != length:
        raise ValueError(f"Both pre_data and post_data must have exactly {length} elements each.")

    rm = pyvisa.ResourceManager()
    smu = rm.open_resource(smu_2ch_addr)
    afg = rm.open_resource(afg_addr)
    afg.write("OUTP1 OFF")
    afg.write(f"OUTP1:LOAD {afg_load_res}")  # Set the load impedance to infinity
    afg.write("SOUR1:FREQ 5")  # Set the pulse frequency to 100 Hz
    afg.write("SOUR1:VOLT 2.50")  # Set the pulse peak-to-peak voltage to 5 V
    afg.write("SOUR1:VOLT:OFFS 1.25")  # Set the voltage offset to 2.5 V (0-5 V swing)
    afg.write("SOUR1:FUNC PULSE")  # Set the source function to pulse
    afg.write("SOURCE1:FUNC:PULS:WIDT 100 ms\n")
    afg.write("SOUR1:BURST:STATE ON")  # Enable burst mode
    afg.write("SOUR1:BURST:MODE TRIGGERED")  # Set burst mode to triggered

    afg.write("SOUR1:BURST:NCYCLES 1")  # Set number of cycles per trigger to 1
    afg.write("TRIGger:SOURce BUS")
    afg.write("OUTP1 ON")
    afg.write("OUTP1:TRIG:SLOPE POSITIVE")  # Set trigger slope to positive


    # smu.write("smua.source.func = smua.OUTPUT_DCVOLTS")
    # smu.write(f"smua.source.levelv = {high_level}")
    # smu.write("smua.source.output = smua.OUTPUT_ON")

    smu.write("smub.source.func = smub.OUTPUT_DCVOLTS")
    smu.write(f"smub.source.levelv = {high_level}")
    smu.write("smub.source.output = smub.OUTPUT_ON")

    print("Starting SMU sequence...")

    #run_clk_sequence(1)

    for i in range(0, length):
        # print(f"Step {i} starts here")


        # time.sleep(t)
        # time.sleep(0.25)
        if arr_low[i]:
            smu.write(f"smub.source.levelv = {high_level}")
        else:
            smu.write(f"smub.source.levelv = {low_level}")

        # time.sleep(t)
        time.sleep(0.05)
        time.sleep(0.05)
        #time.sleep(t)

        #run_clk_sequence(1)
        afg.write("*TRG \n")
        time.sleep(0.05)
        # time.sleep(t)
        # time.sleep(1)

        # time.sleep(t)
        if arr_high[i]:
            smu.write(f"smub.source.levelv = {high_level}")
        else:
            smu.write(f"smub.source.levelv = {low_level}")
        time.sleep(0.1)
        
        # time.sleep(1)
        # time.sleep(t)

    print("SMU sequence complete.")



def run_smu_sequence(length, arr_high, arr_low, t=0.00025):
    if len(arr_high) != length or len(arr_low) != length:
        raise ValueError(f"Both pre_data and post_data must have exactly {length} elements each.")

    rm = pyvisa.ResourceManager()
    smu = rm.open_resource(smu_2ch_addr)
    afg = rm.open_resource(afg_addr)
    afg.write("OUTP1 OFF")
    afg.write(f"OUTP1:LOAD {afg_load_res}")  # Set the load impedance to infinity
    afg.write("SOUR1:FREQ 5")  # Set the pulse frequency to 100 Hz
    afg.write("SOUR1:VOLT 2.50")  # Set the pulse peak-to-peak voltage to 5 V
    afg.write("SOUR1:VOLT:OFFS 1.25")  # Set the voltage offset to 2.5 V (0-5 V swing)
    afg.write("SOUR1:FUNC PULSE")  # Set the source function to pulse
    afg.write("SOURCE1:FUNC:PULS:WIDT 100 ms\n")
    afg.write("SOUR1:BURST:STATE ON")  # Enable burst mode
    afg.write("SOUR1:BURST:MODE TRIGGERED")  # Set burst mode to triggered

    afg.write("SOUR1:BURST:NCYCLES 1")  # Set number of cycles per trigger to 1
    afg.write("TRIGger:SOURce BUS")
    afg.write("OUTP1 ON")
    afg.write("OUTP1:TRIG:SLOPE POSITIVE")  # Set trigger slope to positive


    # smu.write("smua.source.func = smua.OUTPUT_DCVOLTS")
    # smu.write(f"smua.source.levelv = {high_level}")
    # smu.write("smua.source.output = smua.OUTPUT_ON")

    smu.write("smua.source.func = smua.OUTPUT_DCVOLTS")
    smu.write(f"smua.source.rangev = {SMUchA_voltage_range}")
    smu.write(f"smua.source.levelv = {high_level}")
    smu.write("smua.source.output = smua.OUTPUT_ON")

    print("Starting SMU sequence...")

    #run_clk_sequence(1)

    for i in range(0, length):
        # print(f"Step {i} starts here")


        # time.sleep(t)
        # time.sleep(0.25)
        if arr_low[i]:
            smu.write(f"smua.source.levelv = {high_level}")
        else:
            smu.write(f"smua.source.levelv = {low_level}")

        # time.sleep(t)
        time.sleep(0.05)
        time.sleep(0.05)
        #time.sleep(t)

        #run_clk_sequence(1)
        afg.write("*TRG \n")
        time.sleep(0.05)
        # time.sleep(t)
        # time.sleep(1)

        # time.sleep(t)
        if arr_high[i]:
            smu.write(f"smua.source.levelv = {high_level}")
        else:
            smu.write(f"smua.source.levelv = {low_level}")
        time.sleep(0.1)
        
        # time.sleep(1)
        # time.sleep(t)

    print("SMU sequence complete.")