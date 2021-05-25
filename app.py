from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse, Message, Body, Media
from src import drive_db as DB 
from src import response_message as RM

# http://serverhd3.southcentralus.cloudapp.azure.com/sms
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"
    

@app.route("/sms", methods=['POST'])
def sms_reply():
    reply = ''
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    req = request.form
    msg = req.get('Body')
    sender = req.get('WaId')

    # Check the language if the message found a hello, hi or hola
    reply, category = RM.process_response(msg)
    
    # G_Drive connection 
    db_connection = DB.get_connection()
    client_m = {
        'mess':msg,
        'class':category,
    }
    server_m = {
        'mess':reply,
        'class':category
    }
    DB.save_message_pair(sender, client_m, server_m, db_connection)
    del db_connection

    # Create reply

    resp = MessagingResponse()
    message1 = Message()

    message1.body(reply)
    # if the spanish flow flag is true
    
   
    # message2.media('https://demo.twilio.com/owl.png')

    resp.append(message1)
    return str(resp)

if __name__ == "__main__":
    app.run(host='192.168.0.171', port=8080, debug=True)