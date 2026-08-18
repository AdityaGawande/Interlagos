# CLK trimming

vbg_final_trimbit = 8
iref_final_trimbit = 18

import trimming_tests

trimming_tests.Starter()

# for i in range(12,15):
    
trimming_tests.CLK_trim_flow(vbg_final_trimbit,iref_final_trimbit)

for i in range(6,7):
    set_clk_sel_trim(i)
    CLK_trimbit_push(12)
    testmode_exit_safe()
    instr_control.Amplifier_current_check()
    testmode_entry_safe()
    instr_control.dmm_measure_clk(report=1)

trimming_tests.Desert()