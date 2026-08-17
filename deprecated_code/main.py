# Deprecated code

# Comments for future changes and design style
# 1. Make options in switch style
# 2. Make options hierarchical
# 3. Stats are run on timestamped sheets. This is passed to the statistics function.
# 4. Add error handling at this stage with the resulting action being undecided
# 5. Create log files while working on things (separate from terminal output)
# 6. Add safeguards while doing stats and report anomalous readings (outside 10% of mean. Report max percentage difference from mean)
# 7. Change Vsense resistor functions so that they dont affect chip supply on channel 1 and 2
# 8. (concurrent) Trigger, then measure values from the DMMs - check concurrent function
# 9. Create locks on instruments through the code
# 10. Create an archive of generated datasets to save space?
# 11. Make a test vector which gets passed to the internal stats and file management functions


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

# Baseline
# B1. Offset and noise in each DMM
# 2. Gain error in DMMs through SMU - check on paper
# 3. Noise in SMU

# Standard method
# 4. Gain measurement before trimming
# 5. CMRR measurement before trimming
# 6. Trimming with averaging to ensure required certainity
# 7. Reference chip gain and CMRR measurement

# Proposed method
# 8. Gain measurement before trimming - single and averaged
# 9. CMRR measurement before trimming - single and averaged 
# 10. Noise sensitivity through adding noise (before trimming) - discuss with sir
# 11. DUT trimming with required averaging - multiple measurements to check for variation between readings 
# 12. Comparison of trimming measurement and actual measurements - at the end to check for errors

# CSA drift analysis
# 13. Gain+CMRR drift with time in short term and long term at high temp



# Code starts from here
import time
import instr_control
import standard_method
import stats
import baseline_tests as baseline

while True:
    time.sleep(0.2)
    print("\nOptions -")    
    print("1. B1 - Offset drift between measurements and noise in DMMs")
    # print("2. Gain error measurement")
    # print("3. CMRR error measurement")
    print("4. Standard gain measurement")
    print("5. Standard CMRR measurement")
    print("6. Trimming with averaging to ensure required certainity")
    print("7. Reference chip Gain and CMRR measurement")
    # print("8. Calculate honest to god CMRR value")
    # print("9. Update the CSV with values from Google sheet and nothing else")
    print("10. Check all connected instruments")
    # print("11. Burn EFUSE")
    # print("12. DAC2 Sweep")
    print("0. Exit")

    choice = input("Enter your choice: ").strip()

    if choice == '0':
        print("Exiting program.")
        break
    elif choice == '1':
        print("Standard gain measurement")
        # n = int(input("How many times? "))
        baseline.DMM_x3_offset_noise()
    # elif choice == '2':
    #     n = int(input("How many turns? "))
    #     gain_error_measurement(n)
    # elif choice == '3':
    #     n = int(input("How many turns? "))
    #     cmrr_error_measurement(n)
    elif choice == '4':
        print("Standard gain measurement")
        n = int(input("How many times? "))
        # Function to run Standard gain measurement n times and fill it into a csv, (put raw readings into the csv as well)
        standard_method.measure_gain(n)
        # Function to run stats on n measurements - print numbers into the terminal (?send this into the google sheet)
        # stats.single_value_from_csv(n)
        # i2c.trimbits_dump_res()
    elif choice == '5':
        n = int(input("How many times? "))
        # resistor_trim_and_gain_error(n)
    elif choice == '6':
        n = int(input("How many times? "))
        # resistor_trim_and_cmrr_error(n)
    elif choice == '7':
        n = int(input("How many turns? "))
        # combined_gain_cmrr(n)
    # elif choice == '8':
    #     n = int(input("How many turns? "))
    #     honest_to_god_cmrr(n)
    # elif choice == '9':
    #     gsheet_util.csv_file_update()
    #     print("CSV updated!")
    elif choice == '10':
        instr_control.instrument_check()
    # elif choice == '11':
    #     i2c.burn_efuse()
    # elif choice == '12':
    #     start = int(input("DAC value to start from - "))
    #     end = int(input ("DAC value to end at - "))
    #     number = int(input("Number of CMRR readings - "))
    #     DAC2_sweep(start,end,number)
    #     # i2c.burn_efuse()
    else:
        print("Invalid input. Please try again.")