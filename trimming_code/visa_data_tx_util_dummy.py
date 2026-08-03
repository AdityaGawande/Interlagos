# import pyvisa
import time

def run_smu_sequence(length, arr_high, arr_low, t=0.025):
    if len(arr_high) != length or len(arr_low) != length:
        raise ValueError(f"Both pre_data and post_data must have exactly {length} elements each.")

    # arr = pre_data + post_data

    # rm = pyvisa.ResourceManager()
    # smu = rm.open_resource("USB0::0x05E6::0x2636::4428135::INSTR")


    # smu.write("smua.source.func = smua.OUTPUT_DCVOLTS")
    # smu.write("smua.source.levelv = 2")
    # smu.write("smua.source.output = smua.OUTPUT_ON")

    # smu.write("smub.source.func = smub.OUTPUT_DCVOLTS")
    # smu.write("smub.source.levelv = 2")
    # smu.write("smub.source.output = smub.OUTPUT_ON")

    print("Both start at 2V")

    print("Starting SMU sequence...")

    for i in range(0, length):
        print(f"Step {i} starts here")


        # 1. Set smua to source 2V
        # smu.write("smua.source.func = smua.OUTPUT_DCVOLTS")
        # smu.write("smua.source.levelv = 0")
        # smu.write("smua.source.output = smua.OUTPUT_ON")

        # Optional delay between operations
        
        print("Clock is low", end ="; ")
        time.sleep(t)

        if arr_low[i]:
            # smu.write("smub.source.levelv = 2")
            print("Data = high")
        else:
            # smu.write("smub.source.levelv = 0")
            print("Data = low")

        time.sleep(t)

        # smu.write("smua.source.levelv = 2")

        print("Clock is high", end ="; ")

        time.sleep(t)

        if arr_high[i]:
            # smu.write("smub.source.levelv = 2")
            print("Data = high")
        else:
            # smu.write("smub.source.levelv = 0")
            print("Data = low")

        time.sleep(t)        

        # 2. Set smub to source 2V
        # smu.write("smub.source.func = smub.OUTPUT_DCVOLTS")
        # smu.write("smub.source.levelv = 2")
        # smu.write("smub.source.output = smub.OUTPUT_ON")

        # Optional delay before turning off
        # time.sleep(2)

        # 3. Turn OFF both channels
        # smu.write("smua.source.output = smua.OUTPUT_OFF")
        # time.sleep(t)
        # smu.write("smub.source.output = smub.OUTPUT_OFF")

        # 3. Turn OFF both channels
        # if arr[i] :
        #     smu.write("smua.source.levelv = 2")
        #     time.sleep(t)
        #     # smu.write("smub.source.output = smub.OUTPUT_OFF")

    print("SMU sequence complete.")


# seq_without_buf = [1,0,1,0,0,1,0,1,0,1,1,0] # This is 12 bits
# seq = [1]*4 + seq_without_buf + [1]*4   # This is 20 bits


# # First bit needs to be an offset thing always
# arr_high = seq*2
# arr_low = seq*2

# run_smu_sequence(arr_high, arr_low)