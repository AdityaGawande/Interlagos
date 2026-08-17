Interlagos
Intrument control through pyvisa for automated testing
Results can be written to a google sheet
Errors during instrument control are handled
Emails can be sent through the script to notify user about errors/test completion

Issues -
Check Gain/CMRR with new setup
Perform Res trimming

Steps -
Update functions for testmode entry and exit. Make wrappers on top.
Check if codebase is still working after cleanup

Further improvements -
Target the edge of gain error and CMRR based on error bars in the improved method
Use thick wires for connections instead of jumper cables
Make a new print command for printing things into logs - logging in python
Cleanup baseline tests
Add temperature measurements