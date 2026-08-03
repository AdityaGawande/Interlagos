# import amp_full3
import pyvisa
import time

dmm_address_3 = "GPIB0::22::INSTR"

rm = pyvisa.ResourceManager()
dmm = rm.open_resource(dmm_address_3)
time.sleep(0.1)
dmm_v = dmm.query("MEAS:VOLT:DC?")
dmm.close()
val = str(float(dmm_v))

print(val)
