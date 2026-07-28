import instr_top

def measure_gain(n):
    # Change DMM GND from TI chip to PS700 chip
    input("Change DMM GND from TI chip to PS700 chip")
    # instr_top.honest_to_god_cmrr_init()
    instr_top.standard_gain_measure_init()
    
    # Add all of this into the measurement function. Dont close instruments between readings for 100 measurements
    # print(f"Sr.no.\tVoltage error,\tCMRR")
    # for i in range(n):
    #     voltage_error, CMRR = instr_top.honest_to_god_cmrr_single()
    #     # print("Sr.no.\tVoltage error,\tCMRR")
    #     print(f"{i+1},\t{voltage_error:0.6f},\t{CMRR:0.1f}")
    
    # The function invoked here should change SMUch2 current to the limits (taken from constant.py)
    # Put the measurement results and the calculated gain into a csv