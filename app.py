from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse, Message, Body, Media
import utils_sms

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/sms", methods=['POST'])
def sms_reply():
    connv_id = 0
    reply = ''
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body')

    # Check the language if the message found a hello, hi or hola
    lan, spanish_flow, english_flow = utils_sms.language(msg)

    utils_sms.show_ents(msg)
    # Create reply

    resp = MessagingResponse()
    message1 = Message()
    message2 = Message()

    # if the spanish flow flag is true
    if(spanish_flow):
        print('ES')
        message1.body("Muchas gracias por hacer contacto con nosotros")
        reply += utils_sms.spanish_conversation()
    # if the english flow flag is true
    elif(english_flow):
        print('EN')
        message1.body("Thanks for contact us.")
        reply += utils_sms.english_conversation()

    # reply = reply.split("-")
    # for message in reply:
    #     print(message)
    message2.body(reply)

    message2.body("Caso: {}".format(lan))
    message2.media('https://demo.twilio.com/owl.png')

    resp.append(message1)
    resp.append(message2)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)