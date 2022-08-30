from flask import Flask, request, jsonify, render_template
from util import fetch, create, update
from flask_cors import CORS, cross_origin
from flask_mail import Mail, Message

app = Flask(__name__)
mail = Mail(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'do.not.reply.nextstay@gmail.com'
app.config['MAIL_PASSWORD'] = 'pnfkjgpwsueledoz'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route('/')
def hello_world():
    return render_template('loginPage.html')


@app.route('/login', methods=["POST"])
@cross_origin()
def login():
    input_json = request.get_json(force=True)
    # print(input_json)
    data = fetch("CREDENTIALS", input_json)
    dictToReturn = {"authenticatedUser": False}
    if len(data) == 1 and data[0]['isVerified']:
        dictToReturn = {"authenticatedUser": True}
    return jsonify(dictToReturn)


@app.route('/verify', methods=["POST"])
@cross_origin()
def verify():
    input_json = request.get_json(force=True)
    # print(input_json)
    data = fetch("CREDENTIALS", input_json)
    dictToReturn = {"authenticatedUser": False}
    if len(data) == 1:
        payload = {"dataTable": "credentials", "input": {"isverified": True}, "query": {"email": "ddhanu371@gmail.com"}}
        data = update(payload)
        if data['executedSuccessfully']:
            dictToReturn = {"authenticatedUser": True}
    return jsonify(dictToReturn)


@app.route('/signon', methods=["POST"])
@cross_origin()
def signon():
    input_json = request.get_json(force=True)
    data = create(input_json)
    keys = data.keys()
    result = {"executedSuccessfully": True}
    if 'recipients' in keys:
        sendMail(data['recipients'], data['message'], "Verification Code")
    else:
        result = data
    return jsonify(result)


@app.route('/fetchTable', methods=["POST"])
@cross_origin()
def getData():
    dictToReturn = {'data': fetch("STAYS", None)}
    return jsonify(dictToReturn)


@app.route('/manageTable', methods=["POST"])
@cross_origin()
def manageData():
    # print(fetch())
    input_json = request.get_json(force=True)
    dictToReturn = {'data': create(input_json)}
    return jsonify(dictToReturn)


@app.route('/update', methods=["POST"])
@cross_origin()
def updateTable():
    # print(fetch())
    input_json = request.get_json(force=True)
    dictToReturn = {'data': update(input_json)}
    return jsonify(dictToReturn)


@app.route("/sendmail")
def sendMail(recipients, messageBody, subject):
    msg = Message(
        subject,
        sender='do.not.reply.nextstay@gmail.com',
        recipients= recipients
    )
    msg.body = messageBody
    mail.send(msg)
    return 'Sent'
