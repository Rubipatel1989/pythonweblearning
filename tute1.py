import flask
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World Welcome! Patel'

@app.route('/pawan')
def hello():
    return 'Hello, World Welcome! Pawan Patel Kanpur wale'

app.run()