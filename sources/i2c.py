import sources.csv_utils as csv_utils
import sources.gsheet_util as gsheet_util
import time
from sources.constants import t, vref_set_to_testmode_seq_delay, sleep_after_testmode_entry, DUMMY_MODE, i2c_delay_between_commands
import sources.visa_data_tx_util as visa_data_tx_util

delay1 = i2c_delay_between_commands

if (DUMMY_MODE == 1):
    import deprecated_code.relay_power_control_dummy as instr_control
    from deprecated_code.visa_data_tx_util_dummy import run_smu_sequence
else:
    import sources.instr_control as instr_control
    from sources.visa_data_tx_util import run_smu_sequence, run_smu_sequence_v2

def i2c_reg_write_v2(reg_addr_dec, data):
    # Validate length
    if len(data) != 8:
        raise ValueError("Data must be 8-bit sequences")
    # Validate contents
    for bit in data:
        if bit not in (0, 1):
            raise ValueError("Sequences must contain only 0 or 1")

    # convert reg_addr_dec to reg_addr (which is 8-bit binary, with 8 = F2 in binary and 9 = FF in binary)
    if reg_addr_dec == 8:
        reg_addr = [1,1,1,1,0,0,1,0]  # F2 in binary
    elif reg_addr_dec == 9:
        reg_addr = [1,1,1,1,1,1,1,1]  # FF in binary
    else:
        reg_addr = [int(b) for b in format(reg_addr_dec, '08b')]

    # print(reg_addr)
    # print(data)

    offset_p = 3
    offset_n = 3

    start_p = [0]
    start_n = [1]
    stop_p = [1]
    stop_n = [0]
    ack = [1]
    chipid = [1,0,1,1,0,0,0,0]  #8

    arr_high = 5*[1] + offset_p*[1] + start_p + chipid + ack + reg_addr + ack + data + ack + stop_p + offset_n*[1] + 5*[1]
    arr_low = 5*[1] + offset_n*[1] + start_n + chipid + ack + reg_addr + ack + data + ack + stop_n + offset_p*[1] + 5*[1]

    length = 10 + 1 + 8 + 1 + 8 + 1 + 8 + 1 + 1 + offset_p + offset_n

    # Call the provided SMU sequence function
    run_smu_sequence_v2(length, arr_high, arr_low)

# Old version. Kept for reference
def i2c_reg_write(reg_addr_dec, data, t=0.01):
    # Validate length
    if len(data) != 8:
        raise ValueError("Data must be 8-bit sequences")
    # Validate contents
    for bit in data:
        if bit not in (0, 1):
            raise ValueError("Sequences must contain only 0 or 1")

    # convert reg_addr_dec to reg_addr (which is 8-bit binary, with 8 = F2 in binary and 9 = FF in binary)
    if reg_addr_dec == 8:
        reg_addr = [1,1,1,1,0,0,1,0]  # F2 in binary
    elif reg_addr_dec == 9:
        reg_addr = [1,1,1,1,1,1,1,1]  # FF in binary
    else:
        reg_addr = [int(b) for b in format(reg_addr_dec, '08b')]

    print(reg_addr)
    print(data)

    offset_p = 3
    offset_n = 3

    start_p = [0]
    start_n = [1]
    stop_p = [1]
    stop_n = [0]
    ack = [1]
    chipid = [1,0,1,1,0,0,0,0]  #8

    arr_high = 5*[1] + offset_p*[1] + start_p + chipid + ack + reg_addr + ack + data + ack + stop_p + offset_n*[1] + 5*[1]
    arr_low = 5*[1] + offset_n*[1] + start_n + chipid + ack + reg_addr + ack + data + ack + stop_n + offset_p*[1] + 5*[1]

    length = 10 + 1 + 8 + 1 + 8 + 1 + 8 + 1 + 1 + offset_p + offset_n

    # Call the provided SMU sequence function
    run_smu_sequence(length, arr_high, arr_low, t)

# Deprecated
def testmode_entry(t=0.01):
    
    print("Disconnecting Vsense resistor")
    # instr_control.vsense_res_disconnect()
    instr_control.circuit_config_trim()

    print("Set Vref to 8V")
    instr_control.VREF_set(8)
    instr_control.VSUP_voltage_set(1, 5)
    # visa_pwr_update_util.testmode_pwr_set()
    time.sleep(vref_set_to_testmode_seq_delay)

    seq_without_buf = [1,0,1,0,0,1,0,1,0,1,1,0] # This is 12 bits
    seq = [1]*4 + seq_without_buf + [1]*4   # This is 20 bits

    # First bit needs to be an offset thing always
    arr_high = seq*2
    arr_low = seq*2

    # Call the provided SMU sequence function
    run_smu_sequence(40, arr_high, arr_low, t)

    instr_control.SMUchA_output_off()

    # visa_pwr_update_util.testmode_pwr_ref_reset()
    time.sleep(sleep_after_testmode_entry)

def testmode_entry_v2():
    # It is assumed that circuit is in testmode configuration. This is for Trimming Part 1, hence, circuit config commands do not apply.
    # It is assumed that the chip is powered on at 5V. Power resets (if required) need to be performed before running this command.
    instr_control.VREF_set(8)
    testmode_entry_sequence()
    # time.sleep(delay1)
    testmode_entry_sequence()
    # time.sleep(delay1)
    instr_control.VREF_off()
    instr_control.SMU_shutdown()

def testmode_entry_sequence():
    seq_without_buf = [1,0,1,0,0,1,0,1,0,1,1,0] # This is 12 bits
    seq = [1]*4 + seq_without_buf + [1]*4   # This is 20 bits

    # First bit needs to be an offset thing always
    arr_high = seq
    arr_low = seq

    # Call the provided SMU sequence function
    # run_smu_sequence(20, arr_high, arr_low, t)
    visa_data_tx_util.run_smu_sequence_v2(20, arr_high, arr_low)

# Deprecated
def testmode_entry_debug(t=0.01):
    # print("Disconnecting Vsense resistor")
    # instr_control.circuit_config_trim()

    # print("Set Vref to 8V")
    # instr_control.VREF_set(8)
    # instr_control.VSUP_voltage_set(1, 5)
    # time.sleep(vref_set_to_testmode_seq_delay)

    seq_without_buf = [1,0,1,0,0,1,0,1,0,1,1,0] # This is 12 bits
    seq = [1]*4 + seq_without_buf + [1]*4   # This is 20 bits

    # First bit needs to be an offset thing always
    arr_high = seq
    arr_low = seq

    # Call the provided SMU sequence function
    # run_smu_sequence(20, arr_high, arr_low, t)
    visa_data_tx_util.run_smu_sequence_debug(20, arr_high, arr_low, t)

    # instr_control.SMUchA_output_off()

    # time.sleep(sleep_after_testmode_entry)

# Check if this is good enough. Make wrapper on top of this
def testmode_exit():
    # No changes in circuit configuration are performed here
    # I2C command for exiting testmode is present. SMU is turned off at the end.
    reg_addr = 8   #f2
    data = [0,0,0,0,1,1,1,1]    #0f

    # Call the provided SMU sequence function
    i2c_reg_write_v2(reg_addr, data)
    i2c_reg_write_v2(reg_addr, data)

    instr_control.SMU_shutdown()

## Writes into testmode reg to access internal nodes
def testmode_VBG():
    reg_addr = 8   #f2
    data = [0,0,0,0,1,0,0,0]    #08
    # Call the provided SMU sequence function
    i2c_reg_write_v2(reg_addr, data)
    i2c_reg_write_v2(reg_addr, data)

def testmode_IREF():
    reg_addr = 8   #f2
    data = [0,0,0,0,1,1,1,0]    #0E
    # Call the provided SMU sequence function
    i2c_reg_write_v2(reg_addr, data)
    i2c_reg_write_v2(reg_addr, data)

def testmode_CLK():
    reg_addr = 8   #f2
    data = [0,0,0,0,0,0,0,0]    #00
    # Call the provided SMU sequence function
    i2c_reg_write_v2(reg_addr, data)
    i2c_reg_write_v2(reg_addr, data)

## Dumps trimbits
def trimbits_dump():
    regs = csv_utils.csv_reg_value_extraction(0, 0, 8)

    for i in range(0,8):
        # print(f"Writing into reg {i}")
        i2c_reg_write_v2(i, regs[i])
        i2c_reg_write_v2(i, regs[i])

    # time.sleep(2)

def trimbits_dump_osc_core():
    regs = csv_utils.csv_reg_value_extraction(0, 0, 10)

    for i in range(6,8):
        print(f"Writing into reg {i}")
        i2c_reg_write_v2(i, regs[i])
        i2c_reg_write_v2(i, regs[i])

    # time.sleep(2)

def trimbits_dump_res():
    # testmode_entry()

    gsheet_util.csv_file_update()

    regs = csv_utils.csv_reg_value_extraction(0, 0, 10)

    for i in range(2,7):
        print(f"Writing into reg {i}")
        i2c_reg_write_v2(i, regs[i])
        i2c_reg_write_v2(i, regs[i])

    # time.sleep(2)

    # testmode_exit()

def trimbits_dump_vbg():
    regs = csv_utils.csv_reg_value_extraction(0, 0, 10)

    for i in range(0,2):
        # print(f"Writing into reg {i}")
        i2c_reg_write_v2(i, regs[i])
        i2c_reg_write_v2(i, regs[i])

    i = 7
    # print(f"Writing into reg {i}")
    i2c_reg_write_v2(i, regs[i])
    i2c_reg_write_v2(i, regs[i])

    # time.sleep(2)

def trimbits_dump_iref():
    regs = csv_utils.csv_reg_value_extraction(0, 0, 10)

    for i in range(0,2):
        # print(f"Writing into reg {i}")
        i2c_reg_write_v2(i, regs[i])
        i2c_reg_write_v2(i, regs[i])

    i = 7
    # print(f"Writing into reg {i}")
    i2c_reg_write_v2(i, regs[i])
    i2c_reg_write_v2(i, regs[i])

    # time.sleep(2)

def trimbits_dump_clk():
    regs = csv_utils.csv_reg_value_extraction(0, 0, 10)

    i = 1
    # print(f"Writing into reg {i}")
    i2c_reg_write_v2(i, regs[i])
    i2c_reg_write_v2(i, regs[i])

    i = 6
    # print(f"Writing into reg {i}")
    i2c_reg_write_v2(i, regs[i])
    i2c_reg_write_v2(i, regs[i])

    i = 7
    # print(f"Writing into reg {i}")
    i2c_reg_write_v2(i, regs[i])
    i2c_reg_write_v2(i, regs[i])

    # time.sleep(2)

# Do not use unless essential
def trimbits_dump_full():
    regs = csv_utils.csv_reg_value_extraction(0, 0, 10)

    for i in range(0,10):
        print(f"Writing into reg {i}")
        i2c_reg_write(i, regs[i])
        i2c_reg_write(i, regs[i])

    # time.sleep(2)


# Made for debugging. Deprecated
def trimbits_dump_debug():
    regs = csv_utils.csv_reg_value_extraction(1, 0, 10)

    for i in range(0,8):
        print(f"Writing into reg {i}")
        # i2c_reg_write_v2(i, regs[i], t)

    # time.sleep(2)    

# Check before using. Internal functions need to be updated to v2
def burn_efuse():
    input("Change program done bit to 1")
    gsheet_util.csv_file_update()
    # enter testmode
    testmode_entry()
    # Change prog_done bit to 1
    trimbits_dump()
    
    # Change switch to 1
    reg_ff_write(1,0)
    # Change program enable
    reg_ff_write(1,1)
    # wait for 5 sec
    input("continue?")
    
    # Change program enable to 0 + switch to 0
    reg_ff_write(0,0)
    # exit testmode
    testmode_exit()

# Check before using. Internal functions need to be updated to v2
def reg_ff_write(vdd_sw, prog_enable, t = 0.01):
    
    # Validate length
    # if len(data) != 8:
    #     raise ValueError("Data must be 8-bit sequences")
    # # Validate contents
    # for bit in data:
    #     if bit not in (0, 1):
    #         raise ValueError("Sequences must contain only 0 or 1")

    # convert reg_addr_dec to reg_addr (which is 8-bit binary, with 8 = F2 in binary and 9 = FF in binary)
    # if reg_addr_dec == 8:
    #     reg_addr = [1,1,1,1,0,0,1,0]  # F2 in binary
    reg_addr = [1,1,1,1,1,1,1,1]  # FF in binary
    # else:
    #     reg_addr = [int(b) for b in format(reg_addr_dec, '08b')]
    data = [1,1,1,1,1,int(vdd_sw),0,int(prog_enable)]

    print(reg_addr)
    print(data)

    offset_p = 3
    offset_n = 3

    start_p = [0]
    start_n = [1]
    stop_p = [1]
    stop_n = [0]
    ack = [1]
    chipid = [1,0,1,1,0,0,0,0]  #8

    arr_high = 5*[1] + offset_p*[1] + start_p + chipid + ack + reg_addr + ack + data + ack + stop_p + offset_n*[1] + 5*[1]
    arr_low = 5*[1] + offset_n*[1] + start_n + chipid + ack + reg_addr + ack + data + ack + stop_n + offset_p*[1] + 5*[1]

    length = 10 + 1 + 8 + 1 + 8 + 1 + 8 + 1 + 1 + offset_p + offset_n

    # Call the provided SMU sequence function
    run_smu_sequence(length, arr_high, arr_low, t)

# Useless wrapper
def trimbits_dump_regwise(reg):
    regs = csv_utils.csv_reg_value_extraction(1, 0, 8)

    # for i in range(0,8):
    print(f"Writing into reg {reg}")
    i2c_reg_write(reg, regs[reg], t)

    time.sleep(2)

# Debug version. Do not use. v2 is recommended
def i2c_reg_write_debug(reg_addr_dec, data, t=0.01):
    print("DEBUG VERSION IS BEING USED.")
    # Validate length
    if len(data) != 8:
        raise ValueError("Data must be 8-bit sequences")
    # Validate contents
    for bit in data:
        if bit not in (0, 1):
            raise ValueError("Sequences must contain only 0 or 1")

    # convert reg_addr_dec to reg_addr (which is 8-bit binary, with 8 = F2 in binary and 9 = FF in binary)
    if reg_addr_dec == 8:
        reg_addr = [1,1,1,1,0,0,1,0]  # F2 in binary
    elif reg_addr_dec == 9:
        reg_addr = [1,1,1,1,1,1,1,1]  # FF in binary
    else:
        reg_addr = [int(b) for b in format(reg_addr_dec, '08b')]

    # print(reg_addr)
    # print(data)

    offset_p = 3
    offset_n = 3

    start_p = [0]
    start_n = [1]
    stop_p = [1]
    stop_n = [0]
    ack = [1]
    chipid = [1,0,1,1,0,0,0,0]  #8

    arr_high = 5*[1] + offset_p*[1] + start_p + chipid + ack + reg_addr + ack + data + ack + stop_p + offset_n*[1] + 5*[1]
    arr_low = 5*[1] + offset_n*[1] + start_n + chipid + ack + reg_addr + ack + data + ack + stop_n + offset_p*[1] + 5*[1]

    length = 10 + 1 + 8 + 1 + 8 + 1 + 8 + 1 + 1 + offset_p + offset_n

    # Call the provided SMU sequence function
    # run_smu_sequence_debug(length, arr_high, arr_low, t)
