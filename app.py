from flask import Flask, jsonify
from Config import IntRespType, verify_key_decorator
from os import environ
from messages import importantnames, englishwords, customwords
from random import randint, choice
CLIENT_PUBLIC_KEY = environ['CLIENT_PUBLIC_KEY']
# Note to self: When adding to Checkr in Sound's World, ensure to update the interactions endpoint url in DDevs portal, and client public key in railway env vars
app = Flask(__name__)
fullwords = englishwords + (customwords * 2)

@app.route('/', methods=['GET'])
def index():
    return 'Hello World'

@app.route('/responsetest', methods=['GET'])
def responsetest():
    sentencelength = randint(4, 12)
    # sentences always start with a name
    sentence = choice(importantnames)
    n = 0
    while n < sentencelength:
        sentence += f' {choice(fullwords)}'
        n += 1
    return sentence

@app.route('/interactions', methods=['POST'])
@verify_key_decorator(CLIENT_PUBLIC_KEY)
def interactions():
    return jsonify({'type': IntRespType.CHANNEL_MESSAGE_WITH_SOURCE, 'data': {'content': 'Hello World'}})
