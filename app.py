from flask import Flask, request, jsonify, render_template
from util import fetch, create
from flask_cors import CORS, cross_origin
from flask_mail import Mail, Message
import smtplib

# import socket
# hostname=socket.gethostname()
# IPAddr=socket.gethostbyname(hostname)
# print("Your Computer Name is:"+hostname)
# print("Your Computer IP Address is:"+IPAddr)
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'do.not.reply.nextstay@gmail.com'
# app.config['MAIL_PASSWORD'] = 'NextStay@gmail20'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_SERVER']='smtp.mailtrap.io'
# app.config['MAIL_PORT'] = 2525
# app.config['MAIL_USERNAME'] = '97e041d5e367c7'
# app.config['MAIL_PASSWORD'] = 'cfaf5b99f8bafb'
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False
mail = Mail(app)
mail.init_app(app)


@app.route('/')
def hello_world():
    return render_template('loginPage.html')


@app.route('/login', methods=["POST"])
@cross_origin()
def verify():
    input_json = request.get_json(force=True)
    print(input_json)
    data = fetch("CREDENTIALS", input_json)
    dictToReturn = {"authenticatedUser": False}
    if len(data) == 1:
        dictToReturn = {"authenticatedUser": True}
    return jsonify(dictToReturn)


@app.route('/fetchTable', methods=["POST"])
@cross_origin()
def getData():
    # print(fetch())
    # input_json = request.get_json(force=True)
    dictToReturn = {'data': fetch("STAYS", None)}
    return jsonify(dictToReturn)


@app.route('/manageTable', methods=["POST"])
@cross_origin()
def manageData():
    # print(fetch())
    input_json = request.get_json(force=True)
    dictToReturn = {'data': create(input_json)}
    return jsonify(dictToReturn)


@app.route("/sendmail")
def index():
    # msg = Message('Hello', sender='donotreplay@mailtrap.io' ,  recipients = ['bmdhanush05@gmail.com'])
    # msg.body = "This is the email body"
    # mail.send(msg)
    sender = 'from@fromdomain.com'
    receivers = ['to@todomain.com']

    message = """From: From Person <from@fromdomain.com>
   To: To Person <to@todomain.com>
   Subject: SMTP e-mail test

   This is a test e-mail message.
   """

    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receivers, message)
        print("Successfully sent email")
    except smtplib.SMTPException:
        print("Error: unable to send email")
    return "Sent"
