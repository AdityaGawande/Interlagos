
# Calibration constants
G0 = 50

# Code constants
DUMMY_MODE = 0

# Sleep timings
res_connection_delay = 3
vref_set_to_testmode_seq_delay = 5
sleep_after_testmode_entry = 2
testmode_exit_delay = 5


# Instrument constants
# dmm1 for vsense
dmm1_addr = "TCPIP0::10.9.3.214::inst0::INSTR"
# dmm1_addr = "TCPIP0::10.9.3.215::inst0::INSTR"
# dmm2 for vout
dmm2_addr = "TCPIP0::10.9.4.236::inst0::INSTR"
# dmm3 for vcm
dmm3_addr = "TCPIP0::10.9.4.243::inst0::INSTR"
# psu for relay connection/disconnection
psu_addr = "TCPIP0::10.9.3.216::inst0::INSTR"
# smu for Vref and Isense/DATA
smu_2ch_addr = 'TCPIP0::10.9.4.222::inst0::INSTR'
# smu for VCM
smu_bad_addr = "TCPIP::10.9.4.235::inst0::INSTR"
# Function generation for I2C clock
afg_addr = "TCPIP0::10.9.3.234::inst0::INSTR"


# Google sheet constants (Do not change)
csv_filename = 'gsheet_trimbit_values.csv'
# SHEET_ID = '1hF4Snpfwg6-8w03q6VBuWfcwUNAFX5iWZxPIyqwjrc4'
SHEET_ID = '1XKkL62lK_VKFQ7mGQ2JIEgxTk9gaWjvoAuwdnzKqC5g'
google_sheetname1 = "Sheet1"

# Visa transaction constants
t = 0.1     # Changing this will break the I2C commands