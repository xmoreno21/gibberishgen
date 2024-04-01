from flask import Flask, request, jsonify
from Config import IntType, IntRespType, verify_key_decorator
from os import environ
CLIENT_PUBLIC_KEY = environ['CLIENT_PUBLIC_KEY']

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return 'Hello World'

@app.route('/responsetest', methods=['GET'])
def responsetest():
    return 'Hello World'

@app.route('/interactions', methods=['POST'])
@verify_key_decorator(CLIENT_PUBLIC_KEY)
def interactions():
    return jsonify({'type': IntRespType.CHANNEL_MESSAGE_WITH_SOURCE, 'data': {'content': 'Hello World'}})
