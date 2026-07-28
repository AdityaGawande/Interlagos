import pyvisa
import time

# import socket

# ip = '10.9.96.103'
# port = 5025  # typical SCPI port

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((ip, port))

# # Send login credentials (depends on the instrument’s login prompt format)
# s.sendall(b"admin\n")
# s.sendall(b"admin\n")

# # Then send SCPI command
# s.sendall(b"*IDN?\n")

# s.sendall("*RST")

# response = s.recv(4096)
# print(response.decode())

# s.close()


# Initialize VISA resource manager
rm = pyvisa.ResourceManager()

# Connect to Keithley 2450
smu = rm.open_resource("TCPIP::10.9.96.103::inst0::INSTR")

# Optional: Check ID
print(smu.query("*IDN?"))

# Reset and configure source
smu.write("*RST")
smu.write(":SOUR:FUNC VOLT")        # Set to voltage source mode
smu.write(":SOUR:VOLT 2.0")         # Set desired voltage (e.g., 2.0V)
smu.write(":SOUR:VOLT:RANG 20")     # Set voltage range
# smu.write(":SENS:CURR:PROT 0.01")   # Set current limit (compliance) to 10mAsmu.write(':SENS:FUNC "VOLT"')
smu.write(':SENS:VOLT:RANG:AUTO ON')
# smu.write(':TRIG:LOAD CONT')
# smu.write(':OUTP ON')


smu.write("*RST?")
print(smu.query(":READ?"))


# Turn output ON
smu.write(":OUTP ON")
smu.close()

smu = rm.open_resource('TCPIP::10.9.96.103::inst0::INSTR')
print(smu.query("*IDN?"))
smu.close()



