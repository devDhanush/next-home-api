from flask import Flask, request, jsonify, render_template
from util import fetch, create
from flask_cors import CORS, cross_origin
from flask_mail import Mail, Message
import socket
hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)
print("Your Computer Name is:"+hostname)
print("Your Computer IP Address is:"+IPAddr)
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'do.not.reply.nextstay@gmail.com'
app.config['MAIL_PASSWORD'] = 'NextStay@gmail20'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
mail.init_app(app)

@app.route('/')
def hello_world():
    return render_template('loginPage.html')


@app.route('/login', methods=["POST"])
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
   msg = Message('Hello', sender = 'do.not.reply.nextstay@gmail.com', recipients = ['bmdhanush05@gmail.com'])
   msg.body = "This is the email body"
   mail.send(msg)
   return "Sent"