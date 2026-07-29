import pyvisa
import time
from constants import dmm1_addr, dmm2_addr, dmm3_addr
from concurrent.futures import ThreadPoolExecutor
rm = pyvisa.ResourceManager()


def DMM_x3_offset_noise(n,DMM2_range,PLC):

    # PLC = 1

    dmm1 = rm.open_resource(dmm1_addr)
    dmm1.write(":SENS:VOLT:DC:RANGE 0.1")
    dmm1.write(f":SENS:VOLT:DC:NPLC {PLC}")
    dmm1.write("TRIG:SOUR BUS")
    
    dmm2 = rm.open_resource(dmm2_addr)
    dmm2.write(f":SENS:VOLT:DC:RANGE {DMM2_range}")
    dmm2.write(f":SENS:VOLT:DC:NPLC {PLC}")
    dmm2.write("TRIG:SOUR BUS")
    
    dmm3 = rm.open_resource(dmm3_addr)
    dmm3.write(":SENS:VOLT:DC:RANGE 100")
    dmm3.write(f":SENS:VOLT:DC:NPLC {PLC}")
    dmm3.write("TRIG:SOUR BUS")

    print("diff1, diff2, diff3, r11, r12, r21, r22, r31, r32")

    while(n>0):
        DMM_x3_single(dmm1,dmm2,dmm3,PLC)
        n = n-1

    dmm1.close()
    dmm2.close()
    dmm3.close()

    # return results

def DMM_x3_single(dmm1, dmm2, dmm3, PLC):

    constant_delay = 0.5

    dmm1.write("INIT")
    dmm2.write("INIT")
    dmm3.write("INIT")

    with ThreadPoolExecutor() as executor:
        executor.submit(dmm1.write, "*TRG\n")
        executor.submit(dmm2.write, "*TRG\n")
        executor.submit(dmm3.write, "*TRG\n")

    time.sleep(constant_delay+PLC/50)

    r11 = float(dmm1.query("FETCH?"))
    r21 = float(dmm2.query("FETCH?"))
    r31 = float(dmm3.query("FETCH?"))

    dmm1.write("INIT")
    dmm2.write("INIT")
    dmm3.write("INIT")

    with ThreadPoolExecutor() as executor:
        executor.submit(dmm1.write, "*TRG\n")
        executor.submit(dmm2.write, "*TRG\n")
        executor.submit(dmm3.write, "*TRG\n")

    time.sleep(constant_delay+PLC/50)

    r12 = float(dmm1.query("FETCH?"))
    r22 = float(dmm2.query("FETCH?"))
    r32 = float(dmm3.query("FETCH?"))

    print(r11-r12,",", r21-r22,",", r31-r32, ",", r11,",", r12,",", r21,",", r22,",", r31,",", r32)
        

# timestamp = hex(int(time.time()*1000))[2:]

# logfile = open(f"logs/log_{timestamp}.txt","a")

from datetime import datetime
now = str(datetime.now())
print("Test started at", now)
print()
# logfile.write("Test started at ")
# logfile.write(now)
# logfile.write("\n")



length = 40
PLC = 1

print(f"Running at a PLC of {PLC}")
print("DMM2 at voltage range of 0.1V from here -")
DMM_x3_offset_noise(length,0.1,PLC)
print()
# logfile.write("Part 1 completed")
# logfile.write("\n")


print("DMM2 at voltage range of 1V from here -")
DMM_x3_offset_noise(length,1,PLC)
print()
# logfile.write("Part 2 completed")
# logfile.write("\n")


PLC = 10

print(f"Running at a PLC of {PLC}")
print("DMM2 at voltage range of 0.1V from here -")
DMM_x3_offset_noise(length,0.1,PLC)
print()
# logfile.write("Part 3 completed")


print("DMM2 at voltage range of 1V from here -")
DMM_x3_offset_noise(length,1,PLC)
print()
# logfile.write("Part 4 completed")


PLC = 100

print(f"Running at a PLC of {PLC}")
print("DMM2 at voltage range of 0.1V from here -")
DMM_x3_offset_noise(length,0.1,PLC)
print()
# logfile.write("Part 5 completed")


print("DMM2 at voltage range of 1V from here -")
DMM_x3_offset_noise(length,1,PLC)
print()
# logfile.write("Part 6 completed")
