import gsheet_util_new
import time

import pyvisa

rm = pyvisa.ResourceManager()

def measure_dmm(dmm_address):
    dmm = rm.open_resource(dmm_address)
    dmm.timeout = 5000
    dmm.write("*CLS")  # Clear status just in case
    print(dmm.query("*IDN?"))  # Correct SCPI ID query
    dmm_v = dmm.query("MEASure:VOLTage:DC?")
    return dmm_v

# List and verify the address
print(rm.list_resources())

dmm_address = "USB0::0x2A8D::0x1301::MY57210465::INSTR"
x = measure_dmm(dmm_address)
print(x)



'''
# Name of the local file where the sheet is downloaded
filename_csv = 'rough.csv'
# Taken from the URL
google_sheet_id = '1hF4Snpfwg6-8w03q6VBuWfcwUNAFX5iWZxPIyqwjrc4'
# Name of the sheet (not the overall spreadsheet)
google_sheetname = 'TC_G50'

#preset
values_j = [0.001, 0.002, 0.003]
values_d = [0.01, 0.489, 0.02]

values_h = [0.04, 0.134, 0.487]

# gsheet_util_new.write_single_value(google_sheet_id, google_sheetname, cell, value)

arr1 = [13, 25, 39, 53, 66, 79]


t1 = time.time()


for j in range (0,6):
    time.sleep(3)
    for i in range (0,3):
        gsheet_util_new.write_single_value(google_sheet_id, google_sheetname, "D" +str(int(arr1[j])+i) , values_d[i])
        gsheet_util_new.write_single_value(google_sheet_id, google_sheetname, "H" +str(int(arr1[j])+i) , values_h[i]+j*0.005)
        gsheet_util_new.write_single_value(google_sheet_id, google_sheetname, "J" +str(int(arr1[j])+i) , values_j[i])


t2 = time.time()

print(t2-t1)
'''