import time
from sources.instr_control import *
import sources.gsheet_util as gsheet_util

from gspread import Cell
from gspread.utils import a1_to_rowcol

def write_value(cell_value_pairs):
    """
    Write a single value to a specific cell in a Google Sheet.
    """
    client = gsheet_util.authenticate_google_sheets(auth_json)
    worksheet = client.open_by_key(SHEET_ID).worksheet('Live_monitor')

    # row, col = a1_to_rowcol(cell_addr)
    # cell = Cell(row, col, value)

    cells = []
    for cell_addr, value in cell_value_pairs:
        row, col = a1_to_rowcol(cell_addr)
        cells.append(Cell(row, col, value))

    worksheet.update_cells(cells, value_input_option='RAW')

    # worksheet.update_cells([cell], value_input_option='RAW')

    # print(f"Updated cell {cell_addr} with value: {value}")
   
# print("Iq\t\t\tCLK_freq\t\tVBG\t\t\tIREF_current")

clk_freq = 0
iref_current = 0
vbg = 0

def printer(choice):
    while(True):
        # print("clk measurement completed")
        current = dmm_measure_iq()*float(1000*1000)
        # print("iq measurement completed")
        # print("iref measurement completed")
        # print("vbg measurement completed")
        
        if(choice == 1):
            clk_freq = dmm_measure_clk(0)/1000
            iref_current = dmm_measure_iref(0)*(float(1000000000))
            vbg = dmm_measure_vbg(0)
        
        # cell_value_pairs = [
        # ("B6", current),
        # ("B15", clk_freq),
        # ("B24", vbg),
        # ("B33", iref_current)
        # # ("B12", 0),
        # # ("B13", 0),
        # # ("B14", 0),
        # # ("B15", 0),
        # ]
        str1 = f"{current:.3f}uA"
        if(choice == 1):
            str2 = f"{clk_freq:.3f}KHz"
            str3 = f"{vbg:.6f}V"
            str4 = f"{iref_current:.0f}nA"
        
        cell_value_pairs = [
        ("B5", str1)
        ]
        
        if(choice == 1):
            cell_value_pairs = [
            ("B5", str1),
            ("B14", str2),
            ("B23", str3),
            ("B32", str4)
            ]
        
        print(f"{current:.3f}uA\t\t{clk_freq:.3f}KHz\t\t{vbg:.6f}V\t\t{iref_current:.0f}nA")
        # write_value(cell_value_pairs)
        # print("Iteration completed")
        
        # write_value(cell_value_pairs)
        # write_value('B15', clk_freq)
        # write_value('B24', vbg)
        # write_value('B33', iref_current)
        
        # with ThreadPoolExecutor() as executor:
        #     executor.submit(write_value, 'B6', current)
        #     executor.submit(write_value, 'B15', clk_freq)
        #     executor.submit(write_value, 'B24', vbg)
        #     executor.submit(write_value, 'B33', iref_current)
        
        # time.sleep(1)

# choice = int(input("0 for current\n1 for full measurements\nEnter - "))
printer(1)