import pyvisa
import time

# Low and high level of the data and clock in volts
low_level = 0
high_level = 3.3

t = 0.025
def run_smu_sequence(length, arr_high, arr_low, t):
    if len(arr_high) != length or len(arr_low) != length:
        raise ValueError(f"Both pre_data and post_data must have exactly {length} elements each.")

    rm = pyvisa.ResourceManager()
    print(rm)
    print(rm.list_resources())
    smu = rm.open_resource("USB0::0x0957::0x5707::MY53804311::INSTR")
    #smu.write("*RST")
    smu.write("OUTP1 OFF")
    smu.write("SOUR1:FUNC PULSE")  # Set the source function to pulse
    smu.write("SOUR1:FREQ 2")  # Set the pulse frequency to 100 Hz
    smu.write("SOUR1:VOLT 2.5")  # Set the pulse peak-to-peak voltage to 5 V
    smu.write("SOUR1:VOLT:OFFS 1.25")  # Set the voltage offset to 2.5 V (0-5 V swing)
    smu.write("OUTP1:LOAD 50")  # Set the load impedance to 50 ohms
    #smu.write("SOUR1:PULSE:DUTY 50")  # Set the duty cycle to 50%
    smu.write("SOURCE1:FUNC:PULS:WIDT 50 ms\n")
    # smu.write("SOUR1:BURST:MODE TRIGGERED")  # Set burst mode to triggered
    smu.write("SOUR1:BURST:NCYCLES 1")  # Set number of cycles per trigger to 1
    smu.write("SOUR1:BURST:STATE ON")  # Enable burst mode

    smu.write("OUTP1:TRIG:SLOPE POSITIVE")  # Set trigger slope to positive
    smu.write("TRIG1:SOUR BUS")  # Set the trigger source to BUS
    smu.write("SOUR1:BURST:INT:PER 1")  # Set burst period to 1 second
    smu.write("OUTP1 ON")  # Turn the output ON
    
    smu.write("SOURCE1:TRIG:SOUR BUS")
    smu.write("*TRG \n")

    # smu.write("OUTPUT1:STATE OFF")
    # time.sleep(10)

    # smu.write("OUTP1:LOAD INF")

    # smu.write("SOURCE1:FUNCTION PULSE \n")
    # smu.write("SOURCE1:VOLTAGE 2.5\n")
    # smu.write("SOURCE1:VOLTAGE:OFFSET 1.25 \n")

    # smu.write("SOURCE1:FUNC:PULS:WIDT 10 us\n")
    # smu.write("SOURCE1:FUNC:PULS:TRAN:LEADing 10 ns")
    # smu.write("SOURCE1:FUNC:PULS:TRAN:TRA 10 ns")
    # smu.write("SOURCE1:BURST:STATE ON \n")

    # smu.write("SOURCE1:BURS:NCYC 1")
    # smu.write("SOURCE1:BURS:INT:PER 10 ms \n")
    # smu.write("SOURCE1:BURST:MODE TRIGGERED \n")
    # smu.write("OUTPUT1:STATE ON")

    # smu.write("SOURCE1:OUTPUT:TRIGGER:SLOPE POSITIVE")

    # smu.write("SOURCE1:TRIGGER:SLOPE POSITIVE")

   

    #smu.write("TRIGger:IMMediate")
    #smu.write("OUTPUT1:STATE OFF")


run_smu_sequence(1,[0],[0],t)