import pyvisa
import time

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
    

def run_smu_sequence(length, arr_high, arr_low, t=0.05):
    if len(arr_high) != length or len(arr_low) != length:
        raise ValueError(f"Both pre_data and post_data must have exactly {length} elements each.")

    rm = pyvisa.ResourceManager()
    smu = rm.open_resource("USB0::0x05E6::0x2636::4428135::INSTR")

    #afg = rm.open_resource("USB0::0x0957::0x2807::MY58000574::INSTR")
    # afg.write("OUTP1 OFF")

    # afg.write("SOUR1:FREQ 5")  # Set the pulse frequency to 100 Hz
    # afg.write("SOUR1:VOLT 2.50")  # Set the pulse peak-to-peak voltage to 5 V
    # afg.write("SOUR1:VOLT:OFFS 1.25")  # Set the voltage offset to 2.5 V (0-5 V swing)
    # #afg.write("SOUR1:PULSE:DUTY 90")  # Set the duty cycle to 50%
    # afg.write("SOUR1:FUNC PULSE")  # Set the source function to pulse
    # afg.write("SOURCE1:FUNC:PULS:WIDT 100 ms\n")
    # # afg.write("SOUR1:VOLT 3.3")  # Set the pulse peak-to-peak voltage to 5 V
    # # afg.write("SOUR1:VOLT:OFFS 1.65")  # Set the voltage offset to 2.5 V (0-5 V swing)
    # afg.write("OUTP1:LOAD 68")  # Set the load impedance to infinity

    

    # afg.write("SOUR1:BURST:MODE TRIGGERED")  # Set burst mode to triggered
    # afg.write("SOUR1:BURST:NCYCLES 1")  # Set number of cycles per trigger to 1
    # afg.write("SOUR1:BURST:STATE ON")  # Enable burst mode
    # #afg.write("SOUR1:BURST:INT:PER 0.205")  # Set burst period to 0.205 second
    # afg.write("OUTP1 ON")
    # afg.write("*CLS")
    # afg.write("OUTP1:TRIG:SLOPE POSITIVE")  # Set trigger slope to positive
    
    afg = rm.open_resource("USB0::0x0957::0x2807::MY58000574::INSTR")
    afg.write("OUTP1 OFF")
    afg.write("OUTP1:LOAD 68")  # Set the load impedance to infinity
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
        time.sleep(t)
        # time.sleep(1)

        #run_clk_sequence(1)
        afg.write("*TRG \n")
        # time.sleep(t)
        # time.sleep(t)
        # time.sleep(1)

        time.sleep(t)
        if arr_high[i]:
            smu.write(f"smub.source.levelv = {high_level}")
        else:
            smu.write(f"smub.source.levelv = {low_level}")
        time.sleep(2*t)
        # time.sleep(1)
        # time.sleep(t)

    print("SMU sequence complete.")





# import pyvisa
# import time

# # Low and high levels of the data and clock in volts
# low_level = 0
# high_level = 3.3

# def run_smu_sequence(length, arr_high, arr_low, t=0.025):
#     if len(arr_high) != length or len(arr_low) != length:
#         raise ValueError(f"Both pre_data and post_data must have exactly {length} elements each.")

#     rm = pyvisa.ResourceManager()
    
#     # Replace the SMU device with the function generator for channel A (AFG3102)
#     #smu = rm.open_resource("USB0::0x0699::0x034C::C020283::INSTR")  # AFG3102C VISA address
#     smu = rm.open_resource("USB0::0x0957::0x5707::MY53804311::INSTR")
#     smu.write("*RST")  # Reset the AFG3102 to a known state
    
#     # Initialize the function generator (AFG3102C) for voltage control on Channel 1 (smua replacement)
#     smu.write("SOUR1:FUNC PULS")            # Set waveform to Pulse
#     smu.write("SOUR1:FREQ 1E3")             # Frequency = 1 kHz (Adjust if necessary)
#     smu.write("SOUR1:VOLT:AMPL 3.3")        # Amplitude = 3.3V (Adjust if necessary)
#     smu.write("SOUR1:VOLT:OFFS 0")          # Offset = 0V
#     smu.write("SOUR1:PULS:WIDT 10E-3")      # Pulse width = 10ms (Adjust if necessary)
#     smu.write("SOUR1:PULS:PER 20E-3")       # Pulse period = 20ms (Adjust if necessary)
#     smu.write("OUTP1 ON")                   # Enable output on Channel 1 of AFG3102C

#     # Configure SMU (kept for smub) on Channel B (as is)
#     smu_b = rm.open_resource("USB0::0x05E6::0x2636::4428135::INSTR")  # SMU address for Channel B
#     smu_b.write("smub.source.func = smub.OUTPUT_DCVOLTS")
#     smu_b.write(f"smub.source.levelv = {high_level}")
#     smu_b.write("smub.source.output = smub.OUTPUT_ON")

#     print("Starting sequence...")

#     for i in range(0, length):
#         # For Channel A (Function Generator):
#         smu.write(f"SOUR1:VOLT:OFFS {low_level}")  # Set low voltage

#         time.sleep(t)
        
#         # For Channel B (SMU) logic as per arr_low and arr_high
#         if arr_low[i]:
#             smu_b.write(f"smub.source.levelv = {high_level}")
#         else:
#             smu_b.write(f"smub.source.levelv = {low_level}")

#         time.sleep(t)
        
#         # For Channel A (Function Generator):
#         smu.write(f"SOUR1:VOLT:OFFS {high_level}")  # Set high voltage
        
#         time.sleep(t)
        
#         # For Channel B (SMU) logic as per arr_high and arr_low
#         if arr_high[i]:
#             smu_b.write(f"smub.source.levelv = {high_level}")
#         else:
#             smu_b.write(f"smub.source.levelv = {low_level}")

#         time.sleep(t)

#     # Optional: Turn off the outputs after the sequence is complete
#     smu.write("OUTP1 OFF")  # Disable output on AFG3102C
#     smu_b.write("smub.source.output = smub.OUTPUT_OFF")  # Disable output on SMU

#     print("Sequence complete.")

#     smu.close()  # Close the function generator (AFG3102C) session
#     smu_b.close()  # Close the SMU session
#     rm.close()  # Close the VISA session




    