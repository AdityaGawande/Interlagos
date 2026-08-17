Interlagos
Intrument control through pyvisa for automated testing

Issues -
Add trimming functionality - done for VBG, IREF and CLK. Res is remaining
Add error handling - done
Add some feature to send an email or notification on multiple errors - done



Steps -
Update functions for testmode entry and exit. Make wrappers on top.

Further improvements -
Get 2x more triax cables and use 4 wire sensing for higher accuracy from the SMU2ch
Remake the PCB with larger mounting holes, better silkscreen and larger space for soldering
Target the edge of gain error and CMRR based on error bars in the improved method
Use thick wires for connections instead of jumper cables
Make a new print command for printing things into logs - logging in python