# from visa_data_tx_util import run_smu_sequence
import csv_utils
import gsheet_util
import time
from constants import t, testmode_exit_delay, vref_set_to_testmode_seq_delay, sleep_after_testmode_entry, DUMMY_MODE

if (DUMMY_MODE == 1):
    import relay_power_control_dummy as instr_control
    from visa_data_tx_util_dummy import run_smu_sequence
else:
    import instr_control
    from visa_data_tx_util import run_smu_sequence


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

def testmode_exit(t=0.01):
    
    reg_addr = 8   #f2
    data = [0,0,0,0,1,1,1,1]    #0f

    # Call the provided SMU sequence function
    i2c_reg_write(reg_addr, data, t)

    print("Connecting Vsense resistor")
    # instr_control.vsense_res_connect()
    instr_control.circuit_config_amp()
    # instr_control.SMUchA_voltage_set(2.5)
    instr_control.VREF_set(2.5)
    instr_control.VCM_set(0.5)
    # Set Isense to 0 - SMUchB
    instr_control.SMUchB_current_set(0)

    time.sleep(testmode_exit_delay)

def trimbits_dump():
    regs = csv_utils.csv_reg_value_extraction(1, 0, 8)

    for i in range(0,8):
        print(f"Writing into reg {i}")
        i2c_reg_write(i, regs[i], t)

    time.sleep(2)

def trimbits_dump_full():
    regs = csv_utils.csv_reg_value_extraction(1, 0, 10)

    for i in range(0,10):
        print(f"Writing into reg {i}")
        i2c_reg_write(i, regs[i], t)

    time.sleep(2)

def trimbits_dump_res():
    testmode_entry()

    # regs = csv_utils.csv_reg_value_extraction(1, 2, 7)

    # for i in range(2,7):
    #     print(f"Writing into reg {i}")
    #     i2c_reg_write(i, regs[i], t)

    # time.sleep(2)

    # testmode_exit()

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
    



def trimbits_dump_regwise(reg):
    regs = csv_utils.csv_reg_value_extraction(1, 0, 8)

    # for i in range(0,8):
    print(f"Writing into reg {reg}")
    i2c_reg_write(reg, regs[reg], t)

    time.sleep(2)