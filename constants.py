# Calibration constants
G0 = 50

# Measurement settings
VCM_low = 0.5
VCM_high = 4
VREF_voltage = 0.5
VSUP_typical = 5

Isense_high = 5e-5
Isense_low = -Isense_high


# Current and voltage limits for safety
SMUchA_current_limit = 0.001
SMUchB_voltage_limit = 20
VSUP_current_limit = 0.001

# Code constants
DUMMY_MODE = 0

# Sleep timings
res_connection_delay = 3
vref_set_to_testmode_seq_delay = 5
sleep_after_testmode_entry = 2
testmode_exit_delay = 5


# Instrument constants
# dmm1 for vsense
dmm1_addr = "TCPIP0::10.9.0.81::inst0::INSTR"
# dmm1_addr = "TCPIP0::10.9.3.215::inst0::INSTR"
# dmm2 for vout
dmm2_addr = "TCPIP0::10.9.0.82::inst0::INSTR"
# dmm3 for vcm
dmm3_addr = "TCPIP0::10.9.0.83::inst0::INSTR"
# psu for relay connection/disconnection
psu_addr = "TCPIP0::10.9.0.84::inst0::INSTR"
# smu for Vref and Isense/DATA
smu_2ch_addr = 'TCPIP0::10.9.0.86::inst0::INSTR'
# smu for VCM
smu_bad_addr = "TCPIP0::10.9.0.87::inst0::INSTR"
# Function generation for I2C clock
afg_addr = "TCPIP0::10.9.0.85::inst0::INSTR"


# Google sheet constants (Do not change)
csv_filename = 'gsheet_trimbit_values.csv'
# SHEET_ID = '1hF4Snpfwg6-8w03q6VBuWfcwUNAFX5iWZxPIyqwjrc4'
SHEET_ID = '1XKkL62lK_VKFQ7mGQ2JIEgxTk9gaWjvoAuwdnzKqC5g'
google_sheetname1 = "Sheet1"

# Visa transaction constants
t = 0.1     # Changing this will break the I2C commands