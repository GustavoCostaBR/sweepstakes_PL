from googleapiclient.discovery import build
from google.oauth2 import service_account

# Authenticate and build the Drive API client
creds = service_account.Credentials.from_service_account_file('I:/network_share/Gustavo/bolao/teste-spreadsheet2-73bac563f316.json')
drive_service = build('drive', 'v3', credentials=creds)

# ID of the spreadsheet you want to share
spreadsheet_id = '1pGvpgWRA6G6c_RPzLj8RMoSS9Qh7tqheJRiwCI_GUNU'

# Email address you want to share the spreadsheet with
email_address = 'gustavocosta.nh@gmail.com'

# Create a new permission
permission = {
    'type': 'user',
    'role': 'writer',
    'emailAddress': email_address,
}

# Add the permission to the spreadsheet
response = drive_service.permissions().create(fileId=spreadsheet_id, body=permission).execute()

# Print the permission ID
print('Permission ID:', response['id'])
