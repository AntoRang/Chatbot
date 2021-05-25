from random import randint
from . import utils_sms as U_SMS # pylint: disable = relative-beyond-top-level
from . import drive_db as DB # pylint: disable = relative-beyond-top-level


SEMANTICS = DB.get_dataset('semantics')
RESPONSES = DB.get_dataset('responses')


def processing_hello(message: str):
    lan, spanish_flow, english_flow = U_SMS.language(message)
    reply = ''
    if(spanish_flow):
        reply += "Muchas gracias por hacer contacto con nosotros\n"

    # if the english flow flag is true
    elif(english_flow):
        reply+= "Thanks for reaching us. The service at the moment is unavailable.\n"
    del lan
    return reply


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


def process_response(message: str, phone_n: str, google_client: DB.Client):
    category = categorize_msg(message)
    index_resp = randint(0, len(RESPONSES[category])-1)
    last_response = DB.get_last_message(phone_n, google_client)
    print(last_response)
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

    client_m = {'mess': message, 'class': category}
    server_m = {'mess': resp, 'class': category}
    DB.save_message_pair(phone_n, client_m, server_m, google_client)

    return resp
  