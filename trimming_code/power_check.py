import pyvisa

# Your VISA resource address
power_supply = "TCPIP0::10.9.96.107::inst0::INSTR"

# Connect to the power supply
rm = pyvisa.ResourceManager()
smu_vcm = rm.open_resource(power_supply)

# Set channel number and desired voltage
channel = 3
voltage = 5.0  # Example voltage (in Volts)
smu_vcm.write(f"INSTrument:NSELect {channel}")
smu_vcm.write(f"VOLT {voltage}")
smu_vcm.write("CURR 0.01")
smu_vcm.write("OUTP ON")

print(f"Voltage set to {voltage} V and current limit set to 10 mA on channel {channel}")

# Close the connection
smu_vcm.close()
