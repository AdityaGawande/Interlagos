# CLK trimming

vbg_final_trimbit = 12
iref_final_trimbit = 31

import trimming_tests

trimming_tests.Starter()

# for i in range(12,15):
    
trimming_tests.CLK_trim_flow(vbg_final_trimbit,iref_final_trimbit)

trimming_tests.Desert()