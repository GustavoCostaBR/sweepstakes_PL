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
import yaml


def main2(SCOPES2):
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
                'client_secret_902320520879-nv3k45flv1rq57urtus89u4am90ad8qj.apps.googleusercontent.com.json', SCOPES2)
			creds3 = flow.run_local_server(port=8080)
        # Save the credentials for the next run
		with open('token.json', 'w') as token:
			token.write(creds3.to_json())

	return creds3

def forms2(Jogos):
	SCOPES = ['https://www.googleapis.com/auth/forms.body', 'https://www.googleapis.com/auth/spreadsheets']

	# If modifying these scopes, delete the file token.json.
	SCOPES2 = ['https://www.googleapis.com/auth/script.projects', 'https://www.googleapis.com/auth/script.scriptapp', 'https://www.googleapis.com/auth/forms.body', 'https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/forms']

	with open('Configuracoes.yml', 'r') as f:
		data = yaml.load(f, Loader=yaml.FullLoader)

	# SCOPES = ['https://www.googleapis.com/auth/forms', 'https://www.googleapis.com/auth/spreadsheets']
	SERVICE_ACCOUNT_FILE = 'C:/Users/nicol/Downloads/Bolao_2023_24/bolao-premier-league-5a52cb742830.json'
	# SPREADSHEET_ID = '14h7JFsQa5ebEKl3earfrF6NMAcvSCMFtT9J8IZuHLDU'

	# Authenticate with Google using a service account
	creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
	creds2 = service_account.Credentials.from_service_account_file('C:/Users/nicol/Downloads/Bolao_2023_24/bolao-premier-league-5a52cb742830.json')

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
			"title": f"{data['Nome_Rodada']}",
		},
	}


	form = forms_service.forms().create(body=form2).execute()


	form_id = form['formId']

	print(form)

	print(form_id + '\n' )

	# Email address you want to share the form with
	email_address = 'nicolasfhh1992@gmail.com'

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
			'title': f"{data['Nome_Rodada']}"
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
					"title": "Qual é o seu nome? (com sobrenome final)",
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

	# jogos = sys.argv[1:]
	jogos = Jogos
	# jogos = ['Arsenal x Southampton - P1 (PL) - 21/04 - 16:00', 'Fulham x Leeds United - P1 (PL) - 22/04 - 08:30', 'Crystal Palace x Everton - P1 (PL) - 22/04 - 11:00', 'Brentford x Aston Villa - P1 (PL) - 22/04 - 11:00', 'Liverpool x Nottingham Forest - P1 (PL) - 22/04 - 11:00', 'Leicester City x Wolverhampton - P1 (PL) - 22/04 - 11:00', 'Bournemouth x West Ham United - P1 (PL) - 23/04 - 10:00', 'Newcastle United x Tottenham Hotspur - P2 (PL) - 23/04 - 10:00', 'Hearts x Ross County - P1 (SPFL) - 22/04 - 08:30', 'Celtic x Motherwell - P1 (SPFL) - 22/04 - 11:00', 'Aberdeen x Rangers - P1 (SPFL) - 23/04 - 12:30', 'Wigan Athletic x Millwall - P1 (LCH) - 22/04 - 11:00', 'Preston North End x Blackburn Rovers - P2 (LCH) - 22/04 - 13:30', 'West Bromwich Albion x Sunderland - P2 (LCH) - 23/04 - 08:00', 'Manchester City x Sheffield United - P2 (FAC) - 22/04 - 12:45', 'Brighton & Hove Albion x Manchester United - P2 (FAC) - 23/04 - 12:30']

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


	request5 = main2(SCOPES2)

	app_script_service = build('script', 'v1', credentials=request5)

	request = {
		'function': 'updateDestinationSheet',
		'parameters': [form_id, spreadsheet_id],
		'devMode': True  # Set to True for testing, False for production
	}


	response = app_script_service.scripts().run(scriptId='AKfycbzkXvWSY5oaO3NiuZY667l-4rCxFOcbQmzUJsJ9l188OcgKrBTUbnM4aG9e58RMP0XE', body=request).execute()

	# Check the response for errors
	if 'error' in response:
		raise RuntimeError(response['error'])

	id_spreadsheet = {'id': spreadsheet_id}


	with open("info_spreadsheet.yaml", "w", encoding="utf-8") as f:
			yaml.dump(id_spreadsheet, f)