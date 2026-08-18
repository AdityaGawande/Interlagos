# Go through all VBG trim values -> Check stability at a few selected values

from sources.constants import *
import trimming_tests
import sources.instr_control as instr_control

trimming_tests.Starter()

instr_control.VSUP_voltage_reset(active_chip_slot)

trimming_tests.VBG_trim_flow()

trimming_tests.Desert()