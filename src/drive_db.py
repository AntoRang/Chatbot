from datetime import datetime
from json import loads
from gspread import authorize, Client
from gspread.models import Worksheet
from oauth2client.service_account import  ServiceAccountCredentials
from .gs_api_credentials import secure_credentials as SC # pylint: disable = relative-beyond-top-level
from pprint import pprint

LOGS_FOLDER_ID = '1_dCz7T78J33P0bEUoXRHfZyCNLC5UCy6'
DATA_FORMATS = loads(open('src/data_formats.json','r', encoding=SC.ENCODING).read())

def get_connection() -> Client:
    SCOPE = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    dict_cred = SC.get_current_credentials()
    CREDENTIALS = ServiceAccountCredentials.from_json_keyfile_dict(dict_cred,scopes=SCOPE)
    gc = authorize(CREDENTIALS)
    return gc


def get_log_worksheet(phone: str, g_client: Client) -> Worksheet:
    ''' Returns a new Worksheet if not exists, if exists just returns it'''
    data_f = DATA_FORMATS['logs']
    file_list = g_client.list_spreadsheet_files()
    file_list = list(filter(
        lambda file: phone == file['name'],
        file_list
    ))
    worksheet = None
    if len(file_list) == 0:
        spreadsheet =  g_client.create(phone, LOGS_FOLDER_ID)
        worksheet =  spreadsheet.get_worksheet(0)
        worksheet.append_row(data_f)
    elif len(file_list) > 0:
        f_name = file_list[0]['name']
        spreadsheet =  g_client.open(f_name)
        worksheet = spreadsheet.sheet1
    return worksheet


def get_last_message(phone: str, g_client: Client) -> str:
    ''' Function that returns the last message'''
    worksheet = get_log_worksheet(phone, g_client)
    last_mess = None
    try: last_mess = str(worksheet.get_all_records()[-1]['message'])
    except IndexError: pass
    del worksheet
    return last_mess
    

def save_message_pair(phone: str, client_m: dict, server_m: dict, g_client: Client):
    ''' Function that saves client an server messages in the respective phone number log'''
    time_stamp = datetime.now().timestamp()
    worksheet = get_log_worksheet(phone, g_client)
    worksheet.append_rows([
        [time_stamp, client_m['mess'], 'client', client_m['class']],
        [time_stamp, server_m['mess'], 'server', server_m['class']]
    ])
    del worksheet




