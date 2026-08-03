from visa_data_tx_util import run_smu_sequence
#from visa_data_tx_util_dummy import run_smu_sequence


def i2c_reg_write(reg_addr_dec, data, t=0.025):
    
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

def testmode_entry(t=0.025):
    
    seq_without_buf = [1,0,1,0,0,1,0,1,0,1,1,0] # This is 12 bits
    seq = [1]*4 + seq_without_buf + [1]*4   # This is 20 bits

    # First bit needs to be an offset thing always
    arr_high = seq*2
    arr_low = seq*2

    # Call the provided SMU sequence function
    run_smu_sequence(40, arr_high, arr_low, t)

def testmode_exit(t=0.025):
    
    reg_addr = 8   #f2
    data = [0,0,0,0,1,1,1,1]    #0f

    # Call the provided SMU sequence function
    i2c_reg_write(reg_addr, data, t)