# Add import things here
import time
import i2c
import gsheet_util
import instr_top
import instr_control

# Options -
# 1. Update trimbit values from sheet - all values (enter testmode, write bits and exit. Ask for ACK before each step)
# 2. Gain error measurement - ask for how many turns
# 3. CMRR error measurement - ask for how many turns
# 4. Change resistor trim bits - confirm before uploading in a while loop
# 5. Change resistor trim bits and n times Gain error measurement
# 6. Change resistor trim bits and n times CMRR error measurement
# 7. Gain error + CMRR error measurement (using combined formula) - ask for how many turns
# 8. Calculate honest to god CMRR value - ask how many turns
# 9. Update the CSV file with google sheet and nothing else
# 10. Check all the connected instruments one-by-one


def update_trimbit_values():
    print("Updating values from Google sheet...")
    gsheet_util.csv_file_update()
    input("Press Enter to enter test mode...")
    print("Entering test mode...")
    i2c.testmode_entry()
    input("Press Enter to write trim bits from sheet...")
    print("Writing trim bits...")
    i2c.trimbits_dump()
    input("Press Enter to exit test mode...")
    print("Exiting test mode...")
    i2c.testmode_exit()
    instr_top.honest_to_god_cmrr_init()

def update_regwise_values(reg_start, reg_end):
    print("Updating values from Google sheet...")
    gsheet_util.csv_file_update()
    # input("Press Enter to enter test mode...")
    print("Entering test mode...")
    i2c.testmode_entry()
    # input("Press Enter to write trim bits from sheet...")
    print("Writing trim bits...")
    for i in range(reg_start, reg_end):
        i2c.trimbits_dump_regwise(i)
    # input("Press Enter to exit test mode...")
    print("Exiting test mode...")
    i2c.testmode_exit()
    instr_top.honest_to_god_cmrr_init()

def gain_error_measurement(n):
    # Change DMM GND from PS700 chip to TI chip
    input("Change DMM GND from PS700 chip to TI chip")
    
    print("Gain")
    for i in range(0, n):
        G1 = instr_top.gain_error_measurement_single()
        print(f"{G1:0.12f}")

def cmrr_error_measurement(n):
    x = instr_top.CMRR_error_measurement_init()
    # Change DMM GND from TI chip to PS700 chip
    input("Change DMM GND from TI chip to PS700 chip")

    input("Short the input pins on the PS700 board")
    
    # print(f"Running CMRR Error Measurement for {turns} turns...")
    print(f"Sr.no.,\ty-x,\t\tCMRR,\tVoltage error")
    instr_top.gain_error_measurement_init()
    for i in range(0, n):
        error, CMRR, voltage_error = instr_top.CMRR_error_measurement_single(x)
        # print(f"Sr.no.\ty-x \t= \t{error}. CMRR \t= \t{CMRR}")
        print(f"{i+1},\t{error:0.6f},\t{CMRR:0.1f},\t{voltage_error:0.1f}")

def resistor_trim_and_gain_error(n):
    print("Updating values from Google sheet...")
    gsheet_util.csv_file_update()

    input("Disconnect jumper cable between the input pins on the PS700 board")
    print("Changing resistor trim bits...")
    # Enters testmode, writes bits and exits
    i2c.trimbits_dump_res()

    gain_error_measurement(n)

def resistor_trim_and_cmrr_error(n):
    print("Updating values from Google sheet...")
    gsheet_util.csv_file_update()

    input("Unshort the input pins on the PS700 board")
    print("Changing resistor trim bits...")

    i2c.trimbits_dump_res()

    cmrr_error_measurement(n)

def combined_gain_cmrr(n):
    # Change DMM GND from PS700 chip to TI chip
    input("Change DMM GND from PS700 chip to TI chip")

    print(f"Sr.no.\tGainX,\t\tGainY,\t\ty-x error,\tCMRR")
    for i in range(n):
        gainx, gainy, yx_error, CMRR = instr_top.gain_cmrr_error_measurement_single()
        print(f"{i+1},\t{gainx:0.4f},\t{gainy:0.4f},\t{yx_error:0.6f},\t{CMRR:0.1f}")

def honest_to_god_cmrr(n):
    # Change DMM GND from TI chip to PS700 chip
    input("Change DMM GND from TI chip to PS700 chip")
    instr_top.honest_to_god_cmrr_init()
    print(f"Sr.no.\tVoltage error,\tCMRR")
    for i in range(n):
        voltage_error, CMRR = instr_top.honest_to_god_cmrr_single()
        # print("Sr.no.\tVoltage error,\tCMRR")
        print(f"{i+1},\t{voltage_error:0.6f},\t{CMRR:0.1f}")

def DAC2_sweep(start, finish, n):
    for i in range(start, finish+1):
        # Write DAC2 value
        input("Write value to Google sheet")
        update_regwise_values(4,6)
        # CMRR value check for n
        cmrr_error_measurement(n)

while True:
    time.sleep(0.2)
    print("\nOptions -")
    print("1. Update trimbit values from sheet")
    print("2. Gain error measurement")
    print("3. CMRR error measurement")
    print("4. Change resistor trim bits")
    print("5. Change resistor trim bits and n times Gain error measurement")
    print("6. Change resistor trim bits and n times CMRR error measurement")
    print("7. Gain error + CMRR error measurement (one-shot x-y calculation method)")
    print("8. Calculate honest to god CMRR value")
    print("9. Update the CSV with values from Google sheet and nothing else")
    print("10. Check all connected instruments")
    print("11. Burn EFUSE")
    print("12. DAC2 Sweep")
    print("0. Exit")

    choice = input("Enter your choice: ").strip()

    if choice == '0':
        print("Exiting program.")
        break
    elif choice == '1':
        update_trimbit_values()
    elif choice == '2':
        n = int(input("How many turns? "))
        gain_error_measurement(n)
    elif choice == '3':
        n = int(input("How many turns? "))
        cmrr_error_measurement(n)
    elif choice == '4':
        print("Downloading values from Google sheet...")
        gsheet_util.csv_file_update()
        i2c.trimbits_dump_res()
    elif choice == '5':
        n = int(input("How many times? "))
        resistor_trim_and_gain_error(n)
    elif choice == '6':
        n = int(input("How many times? "))
        resistor_trim_and_cmrr_error(n)
    elif choice == '7':
        n = int(input("How many turns? "))
        combined_gain_cmrr(n)
    elif choice == '8':
        n = int(input("How many turns? "))
        honest_to_god_cmrr(n)
    elif choice == '9':
        gsheet_util.csv_file_update()
        print("CSV updated!")
    elif choice == '10':
        instr_control.instrument_check()
    elif choice == '11':
        i2c.burn_efuse()
    elif choice == '12':
        start = int(input("DAC value to start from - "))
        end = int(input ("DAC value to end at - "))
        number = int(input("Number of CMRR readings - "))
        DAC2_sweep(start,end,number)
        # i2c.burn_efuse()
    else:
        print("Invalid input. Please try again.")
