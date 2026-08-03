# import pyvisa

# # Define VISA addresses for the instruments
# smu_address_1 = "USB0::0x05E6::0x2450::04495761::INSTR"  # Keithley 2450
# smu_address_2 = "USB0::0x05E6::0x2460::04323817::INSTR"  # Keithley 2460

# def turn_off_smu_output(rm, address):
#     """Turns off output and closes the connection to an SMU."""
#     try:
#         smu = rm.open_resource(address)
#         idn = smu.query("*IDN?").strip()
#         print(f"Connected to: {idn}")

#         smu.write("OUTP OFF")  # Turn off output
#         print(f"Output turned off for: {idn}")

#         smu.close()
#         print(f"Connection closed for: {idn}\n")
#     except Exception as e:
#         print(f"Failed to turn off SMU at {address}: {e}")

# def main():
#     # Initialize VISA resource manager
#     rm = pyvisa.ResourceManager()

#     # Turn off both instruments
#     turn_off_smu_output(rm, smu_address_1)
#     turn_off_smu_output(rm, smu_address_2)

#     # Close the resource manager
#     rm.close()

# if __name__ == "__main__":
#     main()
import pyvisa

def turn_off_smu_output():
    """Turns off outputs for Keithley 2450 and 2460 SMUs and closes connections."""
    # Define VISA addresses for the instruments
    smu_address_1 = "USB0::0x05E6::0x2450::04495761::INSTR"  # Keithley 2450
    smu_address_2 = "USB0::0x05E6::0x2460::04323817::INSTR"  # Keithley 2460

    try:
        # Initialize VISA resource manager
        rm = pyvisa.ResourceManager()

        for address in [smu_address_1, smu_address_2]:
            try:
                smu = rm.open_resource(address)
                idn = smu.query("*IDN?").strip()
                print(f"Connected to: {idn}")

                smu.write("OUTP OFF")
                print(f"Output turned off for: {idn}")

                smu.close()
                print(f"Connection closed for: {idn}\n")
            except Exception as e:
                print(f"Error with {address}: {e}")

        #rm.close()

    except Exception as e:
        print(f"VISA initialization failed: {e}")
