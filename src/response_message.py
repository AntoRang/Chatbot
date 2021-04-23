from json import loads
from random import randint
from src import utils_sms

RESPONSES = loads(open('src/responses.json', 'r', encoding="utf-8").read())

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
    category = categorize_msg(message)
    index_resp = randint(0, len(RESPONSES[category])-1)
    resp = ''
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

    return resp

    