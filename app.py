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
    """Respond to incoming calls with a simple text message."""

    # G_Drive connection 
    db_connection = DB.get_connection()

    reply = str()
    # Fetch the message
    req = request.form
    msg = str(req.get('Body')).lower()
    sender = req.get('WaId')

    # Process the response to a given message
    try:
        reply = RM.process_response(msg, sender, db_connection)
    except DB.APIError:
        reply = 'Server bussy...\n Please wait 2 minutes after new request'
    del db_connection

    # Create reply
    resp = MessagingResponse()
    message1 = Message()
    message1.body(reply)
    # message1.media('https://demo.twilio.com/owl.png')

    resp.append(message1)
    return str(resp)


if __name__ == "__main__":
    app.run(host='192.168.0.171', port=8080)
    # app.run(host='10.128.0.3', port=8080)
