import pyvisa
import time

# Low and high level of the data and clock in volts
low_level = 0
high_level = 3.3

def run_smu_sequence(length, arr_high, arr_low, t=0.025):
    if len(arr_high) != length or len(arr_low) != length:
        raise ValueError(f"Both pre_data and post_data must have exactly {length} elements each.")

    rm = pyvisa.ResourceManager()
    smu = rm.open_resource("USB0::0x05E6::0x2636::4428135::INSTR")

    smu.write("smua.source.func = smua.OUTPUT_DCVOLTS")
    smu.write(f"smua.source.levelv = {high_level}")
    smu.write("smua.source.output = smua.OUTPUT_ON")

    smu.write("smub.source.func = smub.OUTPUT_DCVOLTS")
    smu.write(f"smub.source.levelv = {high_level}")
    smu.write("smub.source.output = smub.OUTPUT_ON")

    print("Starting SMU sequence...")

    for i in range(0, length):
        # print(f"Step {i} starts here")

        smu.write(f"smua.source.levelv = {low_level}")

        time.sleep(t)
        if arr_low[i]:
            smu.write(f"smub.source.levelv = {high_level}")
        else:
            smu.write(f"smub.source.levelv = {low_level}")

        time.sleep(t)
        smu.write(f"smua.source.levelv = {high_level}")
        
        time.sleep(t)
        if arr_high[i]:
            smu.write(f"smub.source.levelv = {high_level}")
        else:
            smu.write(f"smub.source.levelv = {low_level}")

        time.sleep(t)

    print("SMU sequence complete.")



    