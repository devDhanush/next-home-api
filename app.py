from flask import Flask, request, jsonify
from util import fetch
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def hello_world():
    return 'This is my first API call!'


@app.route('/login', methods=["POST"])
def verify():
    input_json = request.get_json(force=True)
    print(input_json)
    data =  fetch("CREDENTIALS",input_json)
    dictToReturn = {"authenticatedUser": False}
    if(len(data)>0):
        dictToReturn = {"authenticatedUser": True}
    return jsonify(dictToReturn)


@app.route('/fetchTable', methods=["POST"])
@cross_origin()
def getData():
    # print(fetch())
    # input_json = request.get_json(force=True)
    dictToReturn = {'data': fetch("STAYS", None)}
    return jsonify(dictToReturn)