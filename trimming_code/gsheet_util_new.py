import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv
import os

# Google Sheets API setup
def authenticate_google_sheets(credentials_file):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
    client = gspread.authorize(creds)
    return client

def download_sheet_as_csv(sheet_id, sheet_name, output_file):
    client = authenticate_google_sheets('cobalt-list-302320-c192344088ee.json')
    sheet = client.open_by_key(sheet_id).worksheet(sheet_name)
    data = sheet.get_all_values()
    
    # Write data to CSV file
    with open(output_file, mode='w', newline='\n', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    # print(f"Updated {output_file}")

def update_local_files(sheet_id, file_map):
    for sheet_name, local_file in file_map.items():
        if os.path.exists(local_file):
            print(f"Updating {sheet_name}...")
        else:
            print(f"Creating {sheet_name}...")
        download_sheet_as_csv(sheet_id, sheet_name, local_file)


# WRITE FUNCTION
from gspread import Cell
from gspread.utils import a1_to_rowcol

def write_multiple_values(sheet_id, sheet_name, cell_value_pairs):
    """
    Fast batch update: write multiple values to a Google Sheet with no read calls.
    """
    client = authenticate_google_sheets('cobalt-list-302320-c192344088ee.json')
    worksheet = client.open_by_key(sheet_id).worksheet(sheet_name)

    cells = []
    for cell_addr, value in cell_value_pairs:
        row, col = a1_to_rowcol(cell_addr)
        cells.append(Cell(row, col, value))

    worksheet.update_cells(cells, value_input_option='RAW')
    print(f"Updated {len(cells)} cells using fast batch method.")



def read_trim_bits(sheet_name, tab_name, cell):
    # Authenticate using service account (ensure credentials.json is in the same directory or give full path)
    gc = gspread.service_account()

    # Open the spreadsheet by name
    sh = gc.open(sheet_name)

    # Select the specific sheet/tab
    worksheet = sh.worksheet(tab_name)

    # Read the value from the specified cell (e.g., "B2")
    value = worksheet.acell(cell).value

    return value
def read_single_value(sheet_id, sheet_name, cell_address):
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials

    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'cobalt-list-302320-c192344088ee.json', scope
    )
    client = gspread.authorize(creds)
    worksheet = client.open_by_key(sheet_id).worksheet(sheet_name)
    return worksheet.acell(cell_address).value


# Example usage:
#
#print("Value in cell B2:", result)


# def load_file_map_from_csv(csv_filename):
#     file_map = {}

#     try:
#         with open(csv_filename, mode='r', newline='', encoding='utf-8') as csvfile:
#             reader = csv.reader(csvfile)
#             for row in reader:
#                 if len(row) == 2:  # Ensure there are exactly two columns
#                     key, value = row
#                     file_map[key] = value
#                 else:
#                     print(f"Skipping malformed line: {row}")
#     except FileNotFoundError:
#         print(f"File not found: {csv_filename}")
#     except Exception as e:
#         print(f"An error occurred: {e}")

#     return file_map


# if __name__ == "__main__":
#     # Google Sheet ID and mapping of sheet names to local files
#     SHEET_ID = '1hF4Snpfwg6-8w03q6VBuWfcwUNAFX5iWZxPIyqwjrc4'  # Replace with your Google Sheet ID
#     FILE_MAP = {
#         'Sheet5': 'sample.csv'
#         # Add more sheets and files as needed
#     }

#     update_local_files(SHEET_ID, FILE_MAP)