from flask import Flask, request, jsonify
from util import fetch

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'This is my first API call!'


@app.route('/fetchTable', methods=["POST"])
def getData():
    # print(fetch())
    # input_json = request.get_json(force=True)
    dictToReturn = {'data': fetch()}
    return jsonify(dictToReturn)