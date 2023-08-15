from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import yaml

import gspread.utils

def get_values(spreadsheet_id, range_name):
	credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # pylint: disable=maybe-no-member
	try:
		service = build('sheets', 'v4', credentials=credentials)

		result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=range_name).execute()
		rows = result.get('values', [])
		print(f"{len(rows)} rows retrieved")
		return rows
	except HttpError as error:
		print(f"An error occurred: {error}")
		return error

def batch_update_values(spreadsheet_id, data, value_input_option):
	credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

	try:

		service = build('sheets', 'v4', credentials=credentials)



		body = {
            'valueInputOption': value_input_option,
            'data': data
        }

		result = service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id, body=body).execute()


		print(f"{result.get('totalUpdatedCells')} cells updated.")
		return result
	except HttpError as error:
		print(f"An error occurred: {error}")
		return error

with open('Configuracoes.yml', 'r') as f:
	data = yaml.load(f, Loader=yaml.FullLoader)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'I:/network_share/Gustavo/bolao/teste-spreadsheet2-73bac563f316.json'

with open('info_spreadsheet.yaml', 'r') as f:
	data = yaml.load(f, Loader=yaml.FullLoader)

spreadsheet_id = data['id']
range_name = 'Form Responses 1!A1:BM3'

array = get_values (spreadsheet_id, range_name)
# print(array)

print(array)

# data =[]
# for row in range(len(array)):
# 	for col in range(len(array[row])):
# 		if array[row][col] == 'tudo puta':
#             # Replace the old value with the new one
# 			array[row][col] = '2'
# 			# Define the range of the cell to update
# 			a1_notation = gspread.utils.rowcol_to_a1(row+1, col+1)
# 			cell_range = 'Respostas ao formulário 1!' + a1_notation
# 			data.append({'range': cell_range, 'values' : [[array[row][col]]]})





# batch_update_values(spreadsheet_id, data, "USER_ENTERED")


