import standard_tests
from sources.constants import G0 as Gain_ideal

length = 1
PLC = 400


while(True):
    standard_tests.Starter()
    standard_tests.gain_error_measurement(length, Gain_ideal, PLC)
    standard_tests.end_text()

    standard_tests.Starter()
    standard_tests.cmrr_measurement(length, Gain_ideal, PLC)
    standard_tests.end_text()
    print()
    print()
