from random import randint
from datetime import datetime
from googletrans import  Translator
from . import drive_db as DB # pylint: disable = relative-beyond-top-level
from . import gs_translator as GT # pylint: disable = relative-beyond-top-level


DATASETS = DB.get_all_datasets(['semantics','responses','wa_contacts','ex_links']) 
SEMANTICS = DATASETS['semantics']
RESPONSES = DATASETS['responses']
WA_CONTACTS = DATASETS['wa_contacts']
EX_LINKS = DATASETS['ex_links']
del DATASETS
ALLOW_LANGS = ['en','es']

def categorize_msg(message:str, prev_message:dict) -> str:
    ''' Function that sets a category to given message'''
    catego = None
    if prev_message['type'] == 'consulta_pedido':
        catego = 'consulta_pedido2'
    else:
        for category in SEMANTICS.keys():
            sentence_list = SEMANTICS[category]['sentence'].tolist()
            if message in sentence_list:
                catego = category
        if catego == None:
            catego = 'error'
    return catego


def complete_response(text:str, category:str, lang:str) -> str:
    ''' Function that completes a given message'''
    if '*http*' in text:
        if category == 'saludos':
            df = EX_LINKS['refleon.com']
            urls = df[df['lang'] == lang]['url'].tolist()
            url = urls[randint(0, len(urls)-1)]
            text = url.join(text.split('*http*'))
        elif category == 'consulta_pedido2' or category == 'crear_pedido':
            now = datetime.now()
            now_hour = now.hour+1 if now.minute >= 1 else now.hour 
            df = WA_CONTACTS[category]
            df = df[df['lang'] == lang]
            df = df[(df['service_start']<now_hour) & (df['service_end']>now_hour)]
            urls = df['contact_url'].tolist()
            names = df['name'].tolist()
            if len(urls) >= 1:
                rand_index = randint(0, len(urls)-1)
                url = names[rand_index]+ ' ' + urls[rand_index]
                text = url.join(text.split('*http*'))
            else:
                text = 'Por el momento nadie le puede atender, intente en un horario de 8 a 17 hrs'
    return text


def process_response(message: str, phone_n: str, google_client: DB.Client) -> str:
    ''' Function that process a new user message'''
    message, org_lang = GT.any_to_spanish(message)
    last_response = DB.get_last_message(phone_n, google_client)
    category = categorize_msg(message, last_response)
    categ_resp_list = RESPONSES[category]['sentence'].tolist()
    index_resp = randint(0, len(categ_resp_list)-1)
    resp = categ_resp_list[index_resp]

    if org_lang in ALLOW_LANGS:
        resp = complete_response(resp, category, org_lang)
        if org_lang != 'es':
            message = GT.spanish_to_any(message, org_lang)
            resp = GT.spanish_to_any(resp, org_lang)

    client_m = {'mess': message, 'class': category}
    server_m = {'mess': resp, 'class': category}
    DB.save_message_pair(phone_n, client_m, server_m, google_client)

    return resp
