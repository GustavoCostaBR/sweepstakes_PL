import os
import gspread
from apiclient import discovery
from httplib2 import Http
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient import errors
import sys


def main():
	"""Calls the Apps Script API.
	"""
	creds3 = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
	if os.path.exists('token.json'):
		creds3 = Credentials.from_authorized_user_file('token.json', SCOPES2)
    # If there are no (valid) credentials available, let the user log in.
	if not creds3 or not creds3.valid:
		if creds3 and creds3.expired and creds3.refresh_token:
			creds3.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret_882267232515-nci02jnbt3d7h80fi196o16rht6vujii.apps.googleusercontent.com.json', SCOPES2)
			creds3 = flow.run_local_server(port=8080)
        # Save the credentials for the next run
		with open('token.json', 'w') as token:
			token.write(creds3.to_json())

	return creds3


SCOPES = ['https://www.googleapis.com/auth/forms.body', 'https://www.googleapis.com/auth/spreadsheets']

# If modifying these scopes, delete the file token.json.
SCOPES2 = ['https://www.googleapis.com/auth/script.projects', 'https://www.googleapis.com/auth/script.scriptapp', 'https://www.googleapis.com/auth/forms.body', 'https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/forms']

# SCOPES = ['https://www.googleapis.com/auth/forms', 'https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'I:/network_share/Gustavo/bolao/teste-spreadsheet2-73bac563f316.json'
# SPREADSHEET_ID = '14h7JFsQa5ebEKl3earfrF6NMAcvSCMFtT9J8IZuHLDU'

# Authenticate with Google using a service account
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
creds2 = service_account.Credentials.from_service_account_file('I:/network_share/Gustavo/bolao/teste-spreadsheet2-73bac563f316.json')

# Initialize the Google Forms API and Google Sheets API
forms_service = build('forms', 'v1', credentials=creds)
sheets_service = build('sheets', 'v4', credentials=creds)
drive_service = build('drive', 'v3', credentials=creds2)
# Read the column headers from the linked spreadsheet
# sheet_metadata = sheets_service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
# sheet_name = sheet_metadata['sheets'][0]['properties']['title']
# headers = sheets_service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=f'{sheet_name}!1:1').execute().get('values', [])[0]

# Create a new Google Form


form2 = {
    "info": {
        "title": "Rodada_trinta_v_1",
    },
}


form = forms_service.forms().create(body=form2).execute()


form_id = form['formId']

print(form)

print(form_id + '\n' )

# Email address you want to share the form with
email_address = 'gustavocosta.nh@gmail.com'

# Create a new permission
permission = {
    'type': 'user',
    'role': 'writer',
    'emailAddress': email_address
	}

optionalArgs = {
    'sendNotificationEmail': False
  }
# Add the permission to the form
response = drive_service.permissions().create(fileId=form_id, body=permission, **optionalArgs).execute()
# print(response)

# Create a new google spreadsheet
spreadsheet = sheets_service.spreadsheets().create(body={
    'properties': {
        'title': 'Rodada_trinta_v_1'
    }
}).execute()

spreadsheet_id = spreadsheet['spreadsheetId']

print(spreadsheet_id + '\n' )

# Add the permission to the form
response2 = drive_service.permissions().create(fileId=spreadsheet_id, body=permission, **optionalArgs).execute()


page_id = 0

lista_perguntas = []


atualizacion = [
    {
        "createItem": {
            "item": {
                "title": "Qual é o seu nome (com sobrenome final)?",
                "questionItem": {
		            'question': {
			            'required': True,
		                'textQuestion': {}}}},
            "location": {
                "index": 0
            }
        }},
    {
        "createItem": {
            "item": {
                "title": "Qual é a sua senha padrão de aposta? (deverá ser sempre a mesma)",
                "questionItem": {
                    "question": {
                        "required": True,
                        'textQuestion': {}}}
                    },
            "location": {
                "index": 1
        }}
    }]

jogos = sys.argv[1:]

for index in range(len(jogos)):
    parts = jogos[index].split(" x ", 1)
    time1 = parts[0]
    parts2 = parts[1].split(" - ", 1)
    time2 = parts2[0]
    newitem = {
        "createItem": {
            "item": {
                "questionGroupItem": {
                    "questions": [{
                        "required": True,
                        "rowQuestion":{
                            "title": f"{time1}"}},
			    {
				        "required": True,
                        "rowQuestion":{
                            "title": f"{time2}"}}],
                        'grid':
			{
				            'columns':
			     {
				                'type': 'RADIO',
				                'options':
				[{
					                'value':'0'},
				                    {'value': '1'},
				                    {'value': '2'},
				                    {'value': '3'},
				                    {'value': '4'},
				                    {'value': '5'},
				                    {'value': '6'},
				                    {'value': '7'},
				                    {'value': '8'},
				                    {'value': '9'}]}}},
				'title': f"{jogos[index]}"},
		    "location": {
                "index": index+2

                        }}}
    atualizacion.append(newitem)

update = {
    "requests": atualizacion
}



# Add the question to the form
question_setting = forms_service.forms().batchUpdate(
    formId=form_id, body=update).execute()


request5 = main()

app_script_service = build('script', 'v1', credentials=request5)

request = {
    'function': 'updateDestinationSheet',
    'parameters': [form_id, spreadsheet_id],
    'devMode': True  # Set to True for testing, False for production
}


response = app_script_service.scripts().run(scriptId='AKfycbwXk6l4oREUIR-XTshRxZ5Ef6zWCa8dXj80GHLSthMdyxQF1kgjGjaVU52niXKKZBTl', body=request).execute()

# Check the response for errors
if 'error' in response:
    raise RuntimeError(response['error'])

