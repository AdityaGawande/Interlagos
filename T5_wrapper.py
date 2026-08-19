# Check if the trimming is correct

import trimming_tests

vbg_trimbit = 8     # Step gradually from 0 to this
iref_trimbit = 18   # Step directly from 16 to this
clk_trimbit = 12    # Step directly from 31 to this
clk_sel = 6         # Step directly from 0 to this

trimming_tests.trim_check(vbg_trimbit,iref_trimbit,clk_trimbit,clk_sel)