from json import loads
from random import randint
from src import utils_sms

RESPONSES = loads(open('src/responses.json', 'r', encoding="utf-8").read())

def categorize_msg(message:str):
    
    if("hola" in message):
        category_msg = "saludos"
    # elif("pedido" in message):
    #     category_msg = "pedido"
    elif("consultar pedido" in message):
        category_msg = "consulta"
    elif("crear pedido" in message):
        category_msg = "crear_pedido"
    else:
        category_msg = "error"
    return category_msg

def processing_hello(message: str):
    lan, spanish_flow, english_flow = utils_sms.language(message)
    reply = ''
    if(spanish_flow):
        print('ES')
        reply += "Muchas gracias por hacer contacto con nosotros\n"
        # reply += utils_sms.spanish_conversation()
    # if the english flow flag is true
    elif(english_flow):
        print('EN')
        reply+= "Thanks for reaching us. The service at the moment is unable.\n"
        # reply += utils_sms.english_conversation()

    return reply

def process_response(message:str):
    category = categorize_msg(message)
    index_resp = randint(0, len(RESPONSES[category])-1)
    resp = ''
    if(category == "saludos"):
        resp = str(processing_hello(message))
        resp += str(RESPONSES[category][index_resp])
    elif(category == "crear_pedido"):
        asesor = " https://wa.me/qr/HH2HOX4KWQ4PA1" # Asesores
        resp = RESPONSES[category][index_resp] + asesor

    print(resp)
    return resp

    