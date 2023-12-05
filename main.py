import flask
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
local_server = True

with open('config.json','r') as c:
    params = json.load(c)["params"]
app = Flask(__name__)
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']    

db = SQLAlchemy(app)

class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    mobile = db.Column(db.String(13), unique=True, nullable=False)
    message = db.Column(db.String(255), unique=True, nullable=False)
    added = db.Column(db.String(20), unique=True, nullable=False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods = ['GET', 'POST'])
def contact():
    if(request.method == 'POST'):
        ''' Add And Entry To Database'''
        name = request.form.get('name')   
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        message = request.form.get('message')
        entry = Contacts(name = name, email = email, mobile = mobile, message = message)
        db.session.add(entry)
        db.session.commit()

    return render_template('contact.html')

@app.route('/post')
def post():
    return render_template('post.html')

app.run(debug=True)