Interlagos
Intrument control through pyvisa for automated testing

Issues -
Add trimming functionality
Add error handling
Add some feature to send an email or notification on multiple errors



Steps -
[delayed] Get 2x more triax cables and make the setup
[delayed] Get the LAN enabled SMU from chem lab
[skipped] Get gain measurement manually with an external resistor
[skipped] Get gain measurement with the onboard resistor
Make a function to measure the gain and print it
Make a function to measure CMRR and print it
Bring trimming function to this code - abstract away things like gain measurement
    check with dummy instrument_top for gsheet integration

Further improvements -
Get 2x more triax cables and use 4 wire sensing for higher accuracy from the SMU2ch
Remake the PCB with larger mounting holes, better silkscreen and larger space for soldering
Target the edge of gain error and CMRR based on error bars in the improved method
Use thick wires for connections instead of jumper cables