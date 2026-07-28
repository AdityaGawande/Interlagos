import pyvisa
import time
from constants import dmm1_addr, dmm2_addr, dmm3_addr
from concurrent.futures import ThreadPoolExecutor
rm = pyvisa.ResourceManager()


def DMM_x3_offset_noise(n,PLC):

    # PLC = 1

    dmm1 = rm.open_resource(dmm1_addr)
    dmm1.write(":SENS:VOLT:DC:RANGE 0.1")
    # print(":SENS:VOLT:DC:NPLC f{PLC}")
    # print(":SENS:VOLT:DC:NPLC", PLC)
    
    dmm1.write(f":SENS:VOLT:DC:NPLC {PLC}")
    dmm1.write("TRIG:SOUR BUS")
    # dmm1.write("INIT\n")
    # time.sleep(0.1)
    dmm2 = rm.open_resource(dmm2_addr)
    dmm2.write(":SENS:VOLT:DC:RANGE 1")
    dmm2.write(f":SENS:VOLT:DC:NPLC {PLC}")
    # dmm2.write(":SENS:VOLT:DC:NPLC", PLC)
    dmm2.write("TRIG:SOUR BUS")
    # dmm2.write("INIT\n")
    # time.sleep(0.1)
    dmm3 = rm.open_resource(dmm3_addr)
    dmm3.write(":SENS:VOLT:DC:RANGE 100")
    dmm3.write(f":SENS:VOLT:DC:NPLC {PLC}")
    # dmm3.write(":SENS:VOLT:DC:NPLC", PLC)
    dmm3.write("TRIG:SOUR BUS")
    # dmm3.write("INIT\n")
    # time.sleep(0.1)

    # Trigger Voltages from SMUs - concurrency is required. storing their results is not required
    # with ThreadPoolExecutor() as executor:
    #     futures = [
    #         executor.submit(dmm1.write, "*TRG\n"),
    #         executor.submit(dmm2.write, "*TRG\n"),
    #         executor.submit(dmm3.write, "*TRG\n")
    #     ]
    #     results = [float(future.result()) for future in futures]

    # Measure Voltages from SMUs - concurrency is not required
    # with ThreadPoolExecutor() as executor:
    #     futures = [
    #         executor.submit(dmm1.query, "FETCH?"),
    #         executor.submit(dmm2.query, "FETCH?"),
    #         executor.submit(dmm3.query, "FETCH?")
    #     ]
    #     results = [float(future.result()) for future in futures]

    # dmm1.write("INIT")
    # dmm2.write("INIT")
    # dmm3.write("INIT")

    # dmm1.write("*TRG")
    # dmm2.write("*TRG")
    # dmm3.write("*TRG")

    # time.sleep(1+PLC/50)

    # r11 = dmm1.query("FETCH?")
    # r21 = dmm2.query("FETCH?")
    # r31 = dmm3.query("FETCH?")

    # dmm1.write("INIT")
    # dmm2.write("INIT")
    # dmm3.write("INIT")

    # dmm1.write("*TRG")
    # dmm2.write("*TRG")
    # dmm3.write("*TRG")

    # time.sleep(1+PLC/50)

    # r12 = dmm1.query("FETCH?")
    # r22 = dmm2.query("FETCH?")
    # r32 = dmm3.query("FETCH?")

    # print(float(r11)-float(r12),",", float(r21)-float(r22),",", float(r31)-float(r32))
    # # print(float(r11)-float(r12),"\n",r21-r22,"\n",r31-r32)
    print("diff1, diff2, diff3, r11, r12, r21, r22, r31, r32")

    while(n>0):
        DMM_x3_single(dmm1,dmm2,dmm3,PLC)
        n = n-1

    # DMM_x3_single(dmm1,dmm2,dmm3,PLC)
    # DMM_x3_single(dmm1,dmm2,dmm3,PLC)
    # DMM_x3_single(dmm1,dmm2,dmm3,PLC)
    # DMM_x3_single(dmm1,dmm2,dmm3,PLC)
    # DMM_x3_single(dmm1,dmm2,dmm3,PLC)


    # r1 = dmm1.query("FETCH?")
    # r2 = dmm2.query("FETCH?")
    # r3 = dmm3.query("FETCH?")

    # print(r1, r2, r3)

    dmm1.close()
    dmm2.close()
    dmm3.close()

    # return results

def DMM_x3_single(dmm1, dmm2, dmm3, PLC):

    constant_delay = 0.5

    dmm1.write("INIT")
    dmm2.write("INIT")
    dmm3.write("INIT")

    dmm1.write("*TRG")
    dmm2.write("*TRG")
    dmm3.write("*TRG")

    time.sleep(constant_delay+PLC/50)

    r11 = dmm1.query("FETCH?")
    r21 = dmm2.query("FETCH?")
    r31 = dmm3.query("FETCH?")

    dmm1.write("INIT")
    dmm2.write("INIT")
    dmm3.write("INIT")

    dmm1.write("*TRG")
    dmm2.write("*TRG")
    dmm3.write("*TRG")

    time.sleep(constant_delay+PLC/50)

    r12 = dmm1.query("FETCH?")
    r22 = dmm2.query("FETCH?")
    r32 = dmm3.query("FETCH?")

    print(float(r11)-float(r12),",", float(r21)-float(r22),",", float(r31)-float(r32), ",", float(r11),",", float(r12),",", float(r21),",", float(r22),",", float(r31),",", float(r32))
        

DMM_x3_offset_noise(400,100)