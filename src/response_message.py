from json import loads
from random import randint
from src import utils_sms
import os
import pandas as pd
from datetime import datetime

RESPONSES = loads(open('src/responses.json', 'r', encoding="utf-8").read())
ID = "5539518126"
outname = ID + '.csv'
outdir = './src/logs'
fullname = os.path.join(outdir, outname)

def categorize_msg(message:str):
    message = message.lower()

    if("hola" in message or "hello" in message):
        category_msg = "saludos"
    elif("consultar pedido" in message):
        category_msg = "pedido"
    elif("no tengo" in message):
        category_msg = "crear_pedido"
    else:
        category_msg = "error"
    return category_msg

def processing_hello(message: str):
    lan, spanish_flow, english_flow = utils_sms.language(message)
    reply = ''
    if(spanish_flow):
        reply += "Muchas gracias por hacer contacto con nosotros\n"

    # if the english flow flag is true
    elif(english_flow):
        reply+= "Thanks for reaching us. The service at the moment is unavailable.\n"

    return reply

def process_response(message:str):
    msg_time = datetime.now() 
    category = categorize_msg(message)
    index_resp = randint(0, len(RESPONSES[category])-1)
    resp = ''
    Path = os.path.isfile('/scr/logs/'+ ID +'.csv')
    now = datetime.now()    
    if os.path.exists(fullname):
        df = pd.read_csv(fullname)
        last_category = df.status.values
        print(last_category[-1])
        
    if(category == "saludos"):
        resp = processing_hello(message)
        if("Thanks" not in resp):
            resp += RESPONSES[category][index_resp]
    elif(category == "crear_pedido"):
        asesor = " https://wa.me/qr/HH2HOX4KWQ4PA1" # Asesores
        resp = RESPONSES[category][index_resp] + asesor
    elif(category == "pedido"):
        resp = RESPONSES[category][index_resp]
    elif(category == "error"):
        resp = RESPONSES[category][index_resp]
    utils_sms.office_hours("Recepcion", msg_time)
    create_csv(ID, category, now)
    return resp

def create_csv( ID, status, resp_time):
    timestamp = datetime.timestamp(resp_time)
    if os.path.exists(fullname):
        df = pd.read_csv(fullname)
        data = pd.Series([ID, status, timestamp], 
                         index=['ID', 'status', 'timestamp'])
        df = df.append(data, ignore_index=True)
    else:
        data = [ID, status, timestamp]
        columns = ['ID', 'status', 'timestamp']
        df = pd.DataFrame(data, columns).T
    df.to_csv(fullname , index=False)