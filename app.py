from flask import Flask, request, jsonify
from util import fetch
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def hello_world():
    return 'This is my first API call!'


@app.route('/fetchTable', methods=["POST"])
@cross_origin()
def getData():
    # print(fetch())
    # input_json = request.get_json(force=True)
    dictToReturn = {'data': fetch()}
    return jsonify(dictToReturn)