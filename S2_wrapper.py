import standard_tests
from constants import G0 as Gain_ideal

standard_tests.Starter()

length = 10

# PLC = 1
# standard_tests.cmrr_measurement(length, Gain_ideal, PLC)
# print()

# PLC = 10
# standard_tests.cmrr_measurement(length, Gain_ideal, PLC)
# print()

PLC = 100
standard_tests.cmrr_measurement(length, Gain_ideal, PLC)
print()
