
import gspread
from oauth2client.service_account import  ServiceAccountCredentials
from pprint import pprint

SCOPE = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]


CREDENTIALS = ServiceAccountCredentials.from_json_keyfile_name('src/chatbot-313800-510226d75d73.json',scopes=SCOPE)

gc = gspread.authorize(CREDENTIALS)

# for f in gc.list_spreadsheet_files():
#     # pprint(f)
#     # gc.del_spreadsheet(f['id'])
gc.create('test','1_dCz7T78J33P0bEUoXRHfZyCNLC5UCy6')
# wks = gc.open('test').sheet1

# print(wks.get_all_records()) 
