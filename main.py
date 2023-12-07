import flask
from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json
from datetime import datetime


with open('config.json','r') as c:
    params = json.load(c)["params"]

local_server = True
app = Flask(__name__)
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '587',
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = params['gmail_user'],
    MAIL_PASSWORD = params['gmail_password']
)
mail = Mail(app)
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

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False, nullable=True)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    content = db.Column(db.String(1000), unique=True, nullable=False)
    img_file = db.Column(db.String(1000), unique=True, nullable=True)
    date = db.Column(db.String(20), unique=True, nullable=False)

@app.route('/')
def home():
    posts = Posts.query.filter_by().all()[0:4]
    return render_template('index.html', params=params, posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', params=params)

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    if request.method == 'POST':
        #redirect in admin panel
        username = request.form.get('username')
        password = request.form.get('password')

        if(username == params['admin_user'] and password == params['admin_password']):
            #set the session variables
            session['username'] = username

    else:
        return render_template('login.html', params=params)

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

        ''' mail.send_message('New Message from ' + name, sender=email, recipients=[params['gmail_user']], body=message + "\n" + mobile) '''

    return render_template('contact.html', params=params)

@app.route('/post/<string:post_slug>', methods=["GET"])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()

    return render_template('post.html', params=params, post=post)

app.run(debug=True)