from google.oauth2 import service_account
from googleapiclient.discovery import build

# Authenticate and build the Sheets API client
SCOPES = ['https://www.googleapis.com/auth/forms.body', 'https://www.googleapis.com/auth/spreadsheets']
# SCOPES = ['https://www.googleapis.com/auth/forms', 'https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'I:/network_share/Gustavo/bolao/teste-spreadsheet2-73bac563f316.json'

# Authenticate with Google using a service account
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('sheets', 'v4', credentials=creds)

# Create a new spreadsheet
spreadsheet = service.spreadsheets().create(body={
    'properties': {
        'title': 'My New Spreadsheet'
    }
}).execute()

# Print the URL of the newly created spreadsheet
print(f"New spreadsheet created: {spreadsheet['spreadsheetUrl']}")
