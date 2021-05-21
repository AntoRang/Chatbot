import gspread
from oauth2client.service_account import  ServiceAccountCredentials
from pprint import pprint

SCOPE = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]


CREDENTIALS = ServiceAccountCredentials.from_json_keyfile_name('src/chatbot-313800-510226d75d73.json',scopes=SCOPE)

gc = gspread.authorize(CREDENTIALS)

pprint(gc.list_spreadsheet_files())

gc.create('test','0B4fsHHEKTip8UHJaVDNIM2VucFE')
# wks = gc.open('test').sheet1

# print(wks.get_all_records()) 
