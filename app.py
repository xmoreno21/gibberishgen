from flask import Flask, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'
