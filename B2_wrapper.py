import pyvisa
import time
from constants import dmm1_addr, dmm2_addr, dmm3_addr, smu_2ch_addr
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
    
def DMM_x3_GainError(n,voltage,range,PLC, dmm2_range):
    smu = rm.open_resource(smu_2ch_addr)

    # time.sleep(0.1)
    smu.write("smua.source.func = smua.OUTPUT_DCVOLTS")
    smu.write(f"smua.source.levelv = 0")
    smu.write("smua.source.limiti = 0.01")
    smu.write("smua.source.output = smua.OUTPUT_ON")
    
    dmm1 = rm.open_resource(dmm1_addr)
    dmm1.write(f":SENS:VOLT:DC:RANGE {range}")
    dmm1.write(f":SENS:VOLT:DC:NPLC {PLC}")
    dmm1.write("TRIG:SOUR BUS")
    
    dmm2 = rm.open_resource(dmm2_addr)
    dmm2.write(f":SENS:VOLT:DC:RANGE {dmm2_range}")
    dmm2.write(f":SENS:VOLT:DC:NPLC {PLC}")
    dmm2.write("TRIG:SOUR BUS")
    
    dmm3 = rm.open_resource(dmm3_addr)
    dmm3.write(f":SENS:VOLT:DC:RANGE {range}")
    dmm3.write(f":SENS:VOLT:DC:NPLC {PLC}")
    dmm3.write("TRIG:SOUR BUS")

    print("GE1, GE2, GE3, ratio12, ratio13, ratio23, diff1, diff2, diff3, r11, r12, r21, r22, r31, r32")

    # Perform measurements here for n times
    while(n>0):
        DMM_x3_GE_single(dmm1,dmm2,dmm3,smu,voltage,PLC)
        n = n-1

    dmm1.close()
    dmm2.close()
    dmm3.close()
    
    smu.write("smua.source.output = smub.OUTPUT_OFF")
    smu.close()
    time.sleep(1)

    
def DMM_x3_GE_single(dmm1, dmm2, dmm3, smu, voltage, PLC):
    
    constant_delay = 0.5
    
    smu.write(f"smua.source.levelv = {voltage}")
    
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

    smu.write(f"smua.source.levelv = -{voltage}")

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

    reading1 = r11-r12
    reading2 = r21-r22
    reading3 = r31-r32

    ratio12 = reading1/reading2
    ratio13 = reading1/reading3
    ratio23 = reading2/reading3

    print(ratio12-1,",", ratio13-1,",", ratio23-1, ",", ratio12,",", ratio13,",", ratio23, ",", reading1,",", reading2,",", reading3, ",", r11,",", r12,",", r21,",", r22,",", r31,",", r32)
    

# timestamp = hex(int(time.time()*1000))[2:]

# logfile = open(f"logs/log_{timestamp}.txt","a")

from datetime import datetime
now = str(datetime.now())
print("Test started at", now)
# logfile.write("Test started at ")
# logfile.write(now)
# logfile.write("\n")



length = 4

voltage = 0.005
range = 0.1

PLC = 1
print(f"Input voltage = {voltage}")
print(f"Running at a PLC of {PLC}")
DMM_x3_GainError(length,voltage,range,PLC,range)
print()

PLC = 10
print(f"Input voltage = {voltage}")
print(f"Running at a PLC of {PLC}")
DMM_x3_GainError(length,voltage,range,PLC,range)
print()

PLC = 100
print(f"Input voltage = {voltage}")
print(f"Running at a PLC of {PLC}")
DMM_x3_GainError(length,voltage,range,PLC,range)
print()


voltage = 0.050
range = 0.1

PLC = 1
print(f"Input voltage = {voltage}")
print(f"Running at a PLC of {PLC}")
DMM_x3_GainError(length,voltage,range,PLC,range)
print()

PLC = 10
print(f"Input voltage = {voltage}")
print(f"Running at a PLC of {PLC}")
DMM_x3_GainError(length,voltage,range,PLC,range)
print()

PLC = 100
print(f"Input voltage = {voltage}")
print(f"Running at a PLC of {PLC}")
DMM_x3_GainError(length,voltage,range,PLC,range)
print()


voltage = 0.500
range = 1

PLC = 1
print(f"Input voltage = {voltage}")
print(f"Running at a PLC of {PLC}")
DMM_x3_GainError(length,voltage,range,PLC,range)
print()

PLC = 10
print(f"Input voltage = {voltage}")
print(f"Running at a PLC of {PLC}")
DMM_x3_GainError(length,voltage,range,PLC,range)
print()

PLC = 100
print(f"Input voltage = {voltage}")
print(f"Running at a PLC of {PLC}")
DMM_x3_GainError(length,voltage,range,PLC,range)
print()


print("Special case for Gain error across ranges")
voltage = 0.005
range = 0.1
dmm2_range = 1

PLC = 1
print(f"Input voltage = {voltage}")
print(f"Running at a PLC of {PLC}")
DMM_x3_GainError(length,voltage,range,PLC,dmm2_range)
print()

PLC = 10
print(f"Input voltage = {voltage}")
print(f"Running at a PLC of {PLC}")
DMM_x3_GainError(length,voltage,range,PLC,dmm2_range)
print()

PLC = 100
print(f"Input voltage = {voltage}")
print(f"Running at a PLC of {PLC}")
DMM_x3_GainError(length,voltage,range,PLC,dmm2_range)
print()