# CM_voltage = 1.5 

# isense=0.002
####power supply

# import pyvisa
import time

def testmode_pwr_set():

    print("Vref set to 8V")
    # '''
    # # Initialize the VISA resource manager
    # rm = pyvisa.ResourceManager()

    # # Define the VISA address for your Keysight E36231A
    # visa_address = "USB0::0x2A8D::0x2F02::MY61002591::INSTR"  # Update this with your actual VISA address

    # # Open the connection to the power supply
    # psu = rm.open_resource(visa_address)

    # # Optional: Check if the connection is successful
    # print("Connected to:", psu.query("*IDN?").strip())

    # psu.write("RST")
    # psu.write("INST:NSEL 1")
    # psu.write("VOLT 5")
    # psu.write("CURR 0.01")
    # psu.write("OUTP ON")
    # '''

    # # ###### smu for current and vref


    # # import pyvisa
    # # import time

    # # Initialize VISA and connect to Keithley 2636B via USB
    # rm = pyvisa.ResourceManager()

    # # Connect to the Keithley 2636B using the correct VISA address
    # smu = rm.open_resource('TCPIP0::10.9.96.113::inst0::INSTR')  # Replace with your actual VISA address

    # # Verify connection (optional)
    # print("Connected to:", smu.query("*IDN?").strip())

    # # Reset the device to a known state
    # smu.write("*RST")
    time.sleep(1)  # Allow time for the reset

    # vref=8

    # # # Configure Channel B (source current, limit voltage)
    # # smu.write("smub.source.func = smub.OUTPUT_DCAMPS")     # Source DC current
    # # smu.write(f"smub.source.leveli = {isense}")                # Set current to 2 mA
    # # smu.write("smub.source.limitv = 10")                   # Voltage limit = 10 V
    # # smu.write("smub.source.output = smub.OUTPUT_ON")       # Enable output

    # # Configure Channel A(source voltage, limit current)
    # smu.write("smua.source.func = smua.OUTPUT_DCVOLTS")    # Source DC voltage
    # smu.write(f"smua.source.levelv = {vref}")                 # Set voltage to 5 V
    # smu.write("smua.source.limiti = 0.0005")                  # Current limit = 500 mA
    # smu.write("smua.source.output = smua.OUTPUT_ON")       # Enable output

    # smu.close()
    # #rm.close()

def vref_set(ch1_voltage, ch2_voltage):
    print(f"Ch1 = {ch1_voltage}. Ch2 = {ch2_voltage}. ")
    # '''
    # # Initialize the VISA resource manager
    # rm = pyvisa.ResourceManager()

    # # Define the VISA address for your Keysight E36231A
    # visa_address = "USB0::0x2A8D::0x2F02::MY61002591::INSTR"  # Update this with your actual VISA address

    # # Open the connection to the power supply
    # psu = rm.open_resource(visa_address)

    # # Optional: Check if the connection is successful
    # print("Connected to:", psu.query("*IDN?").strip())

    # psu.write("RST")
    # psu.write("INST:NSEL 1")
    # psu.write("VOLT 5")
    # psu.write("CURR 0.01")
    # psu.write("OUTP ON")
    # '''

    # # ###### smu for current and vref


    # # import pyvisa
    # # import time

    # # Initialize VISA and connect to Keithley 2636B via USB
    # rm = pyvisa.ResourceManager()

    # # Connect to the Keithley 2636B using the correct VISA address
    # smu = rm.open_resource('TCPIP0::10.9.96.113::inst0::INSTR')  # Replace with your actual VISA address

    # # Verify connection (optional)
    # print("Connected to:", smu.query("*IDN?").strip())

    # # Reset the device to a known state
    # smu.write("*RST")
    time.sleep(1)  # Allow time for the reset

    # # vref=8

    # # # Configure Channel B (source current, limit voltage)
    # # smu.write("smub.source.func = smub.OUTPUT_DCAMPS")     # Source DC current
    # # smu.write(f"smub.source.leveli = {isense}")                # Set current to 2 mA
    # # smu.write("smub.source.limitv = 10")                   # Voltage limit = 10 V
    # # smu.write("smub.source.output = smub.OUTPUT_ON")       # Enable output

    # # Configure Channel A(source voltage, limit current)
    # smu.write("smua.source.func = smua.OUTPUT_DCVOLTS")    # Source DC voltage
    # smu.write(f"smua.source.levelv = {ch1_voltage}")                 # Set voltage to 5 V
    # smu.write("smua.source.limiti = 0.0005")                  # Current limit = 500 mA
    # smu.write("smua.source.output = smua.OUTPUT_ON")       # Enable output

    # # Configure Channel B(source voltage, limit current)
    # smu.write("smub.source.func = smua.OUTPUT_DCVOLTS")    # Source DC voltage
    # smu.write(f"smub.source.levelv = {ch2_voltage}")                 # Set voltage to 5 V
    # smu.write("smub.source.limiti = 0.0005")                  # Current limit = 500 mA
    # smu.write("smub.source.output = smua.OUTPUT_ON")       # Enable output

    # smu.close()
    # #rm.close()


def testmode_pwr_ref_reset():
    print("SMU CH-A output turned off")

    # # Initialize VISA and connect to Keithley 2636B via USB
    # rm = pyvisa.ResourceManager()

    # # Connect to the Keithley 2636B using the correct VISA address
    # smu = rm.open_resource('TCPIP0::10.9.96.113::inst0::INSTR')  # Replace with your actual VISA address

    # # Verify connection (optional)
    # print("Connected to:", smu.query("*IDN?").strip())

    # smu.write("smua.source.output = smua.OUTPUT_OFF")       # Enable output
    
    # smu.close()
    # #rm.close()





#### function genrator for Dc common mode



# import pyvisa
# rm = pyvisa.ResourceManager()
# gen = rm.open_resource("USB0::0x0957::0x5707::MY53804311::INSTR")
# gen.timeout = 5000

# gen.write("OUTPut OFF")                            # Turn off output
# gen.write("OUTP:LOAD INF")                         # High impedance
# gen.write("FUNCtion:SHAPe DC")                     # Set waveform to DC
# gen.write(f"SOUR1:VOLT:OFFS {CM_voltage}")         # Set DC voltage using variable
# gen.write("OUTPut ON")                             # Enable output


# import pyvisa
# import time
# from concurrent.futures import ThreadPoolExecutor

# # Initialize the VISA resource manager
# rm = pyvisa.ResourceManager()

# # Function to measure voltage and calculate average for a given SMU
# def measure_and_average(smu_address, num_measurements=5):
#     smu = rm.open_resource(smu_address)
#     # Optional: Check if the connection is successful
#     #print("Connected to:", smu.query("*IDN?").strip())
    
#     vaverage = 0.0
#     for i in range(1, num_measurements + 1):
#         #smu.write("smu.measure.func = smu.MEASURE_DCVOLTS")  # Set to measure DC Voltage
#         voltage_str = smu.query("MEAS:VOLT?")  # Query the voltage as string
#         voltage = float(voltage_str)  # Convert to float
#         print(f"Measured Voltage {i} from {smu_address}: {voltage:.6f} V")
#         vaverage += voltage
#         time.sleep(0.000001)  # 1 second delay

#     vaverage /= num_measurements
#     print(f"\nAverage Voltage from {smu_address}: {vaverage:.6f} V")
#     return vaverage


# # SMU addresses (Replace these with your actual addresses)
# smu_address_1 = "USB0::0x05E6::0x2450::04495761::INSTR"
# smu_address_2 = "USB0::0x05E6::0x2460::04323817::INSTR"

# # Create a thread pool to handle parallel tasks
# with ThreadPoolExecutor() as executor:
#     # Execute measure_and_average for both SMUs in parallel
#     futures = [
#         executor.submit(measure_and_average, smu_address_1),
#         executor.submit(measure_and_average, smu_address_2)
#     ]
    
#     # Retrieve results (average voltage for each SMU)
#     results = [future.result() for future in futures]

# # Optionally, print the results for both SMUs
# print(f"\nFinal Average Voltages:")
# print(f"SMU 1 Average Voltage: {results[0]:.6f} V")
# print(f"SMU 2 Average Voltage: {results[1]:.6f} V")


