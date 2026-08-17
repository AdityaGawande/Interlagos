# Calibration constants
G0 = 50
active_chip_slot = 2
active_chip_id = 3


# Measurement settings
VCM_low = 0.5
VCM_high = 4
VREF_voltage = 2.5
VSUP_typical = 5

Isense_high = 5e-3
Isense_low = -Isense_high


# Current and voltage limits for safety
SMUchA_current_limit = 0.0002
SMUchB_voltage_limit = 20
VSUP_current_limit = 0.001
relay_current_limit = 0.1
SMUchA_voltage_range = 20
SMUbad_voltage_range = 20
SMUbad_current_limit = 0.000025
SMUbad_current_range = 0.0001

# Code constants
DUMMY_MODE = 0

# Sleep timings
res_connection_delay = 3
vref_set_to_testmode_seq_delay = 5
sleep_after_testmode_entry = 2
testmode_exit_delay = 5
sleep_after_voltage_change = 1
sleep_after_resource_open = 0.1
sleep_between_VSUP_power_reset = 0.3


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
SHEET_ID = '1d5e6bYR3UWXNtU9GqvDx5CAbm5iQKSkFBRPAPimTJb8'
google_sheetname1 = "Python_sheet"
auth_json = 'cobalt-list-302320-c192344088ee.json'

# Visa transactions
t = 0.1     # Was critical for I2C. Deprecated now
afg_load_res = 67

# I2C voltages and timing
i2c_high_level = 2
i2c_low_level = 0.005
i2c_freq = 100
i2c_time_period = 1/i2c_freq
i2c_duty_cycle = 0.5
i2c_delay_between_commands = 0.5

# Error handling
error_handle_retries = 20
error_handle_delay = 0.2