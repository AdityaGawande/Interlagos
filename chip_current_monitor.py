import time
from sources.instr_control import Amplifier_current_check
while(True):
    Amplifier_current_check()
    time.sleep(1)