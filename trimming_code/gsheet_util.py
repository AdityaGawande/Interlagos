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