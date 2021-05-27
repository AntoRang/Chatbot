from json import loads
from datetime import datetime
from pandas import DataFrame
from gspread import authorize, Client
from gspread.models import Worksheet, Spreadsheet
from oauth2client.service_account import  ServiceAccountCredentials
from .gs_api_credentials import secure_credentials as SC # pylint: disable = relative-beyond-top-level

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


def create_log(phone: str, g_client: Client) -> Worksheet:
    ''' Function that returns a new log file worksheet'''
    data_f = DATA_FORMATS['logs']
    spreadsheet =  g_client.create(phone, LOGS_FOLDER_ID)
    worksheet =  spreadsheet.get_worksheet(0)
    worksheet.append_row(data_f)
    return worksheet


def get_log_worksheet(phone: str, g_client: Client) -> Worksheet:
    ''' Returns a new Worksheet if not exists, if exists just returns it'''
    file_list = g_client.list_spreadsheet_files()
    file_list = list(filter(
        lambda file: phone == file['name'],
        file_list
    ))
    worksheet = None
    if len(file_list) == 0:
        worksheet = create_log(phone, g_client)
    elif len(file_list) == 1:
        f_name = file_list[0]['name']
        spreadsheet =  g_client.open(f_name)
        worksheet = spreadsheet.sheet1
    else:
        for f in file_list:
            g_client.del_spreadsheet(f['id'])
        worksheet = create_log(phone, g_client)
    return worksheet


def get_last_message(phone: str, g_client: Client) -> dict:
    ''' Function that returns the last message'''
    data_f = DATA_FORMATS['logs']
    worksheet = get_log_worksheet(phone, g_client)
    last_mess = dict()
    try: last_mess = worksheet.get_all_records()[-1]
    except IndexError: last_mess = {col:None for col in data_f}
    del worksheet
    return last_mess
    

def save_message_pair(phone: str, client_m: dict, server_m: dict, g_client: Client):
    ''' Function that saves client an server messages in the respective phone number log'''
    time_stamp = datetime.now().isoformat()
    worksheet = get_log_worksheet(phone, g_client)
    worksheet.append_rows([
        [time_stamp, client_m['mess'], 'client', client_m['class']],
        [time_stamp, server_m['mess'], 'server', server_m['class']]
    ])
    del worksheet


def get_dataset(dataset_file: str, g_client: Client) -> dict:
    ''' Function that returns the static dict of datasets as pandas.DataFrame'''
    data_f = DATA_FORMATS[dataset_file]
    spreadsheet = g_client.open(dataset_file)
    worksheets = [wk.title for wk in spreadsheet.worksheets()]
    master_dict = dict()
    for wk_name in worksheets:
        wk = spreadsheet.worksheet(wk_name)
        master_dict.update({wk_name:{col:list() for col in data_f}})
        for rec in wk.get_all_records():
            for col in rec.keys():
                master_dict[wk_name][col].append(rec[col])
        del wk
        master_dict[wk_name] = DataFrame(master_dict[wk_name])
    del spreadsheet
    return master_dict


def get_all_datasets(d_files: list) -> dict:
    ''' Function that returns the server datasets as dict of dicts'''
    gc = get_connection()
    data = {file:dict() for file in d_files}
    for file in d_files:
        data[file] = get_dataset(file, gc)
    del gc
    return data

