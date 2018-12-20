import jwt

from flask import jsonify, Blueprint, request, render_template
import json
from utils.dbutils import get_db_session
import utils.utils as utils
import bcrypt
from db.user import User
import random 
import smtplib 

import httplib2
import os
import base64
import uuid

login_routes = Blueprint('login_routes', __name__)

@login_routes.route('/api/login', methods=['POST'])
def post_login():
    data = request.values
    if data is None or len(data)==0:
        data = request.get_json(force=True)

    username = data.get('username')
    if username is None:
        return jsonify(status='fail', message='must provide a username')

    password = data.get('password')

    allowed_status = ['user', 'admin', 'sadmin']

    if password is None:
        return jsonify(status='fail', message='password not provided')

    session = get_db_session()
    user = session.query(User).filter_by(email=username).first()
    if user is None:
        user = session.query(User).filter_by(phone_number=username).first()
 
    if user is None:
        return jsonify(status='fail', message='user does not exist')
    
    if user.salt is None:
        print("user {} is not yet confirmed but trying to login".format(user.email))
        return jsonify(status='fail', message='user has not been confirmed')

    if user.status not in allowed_status:
        print("ERROR: Attempt to use disabled account (id:{} - name:{} - status: {})".format(user.id, user.name, user.status))
        return jsonify(status='fail', message='account has been disabled')

    hashedpass = bcrypt.hashpw(password.encode(), user.salt.encode())

    if hashedpass.decode() != user.password:
        return jsonify(status='fail', message='password incorrect')

    secret = utils.get_jwt_secret()
    if user.email is not None:
        jwttoken = jwt.encode({'username': user.email}, secret, algorithm='HS256')
    elif user.phone_number is not None:
        jwttoken = jwt.encode({'username': user.phone_number}, secret, algorithm='HS256')
       
    return jsonify(status='ok', token=jwttoken.decode())

@login_routes.route('/login')
def get_login_page():
    rand = None
    app = utils.get_app()
    if app.debug != False:
        rand = random.random()

    template_name = 'login.html'

    # if utils.is_on_mobile(request.headers.get('User-Agent')):
    #     template_name = 'mobile/login.mobile.html'

    return render_template(template_name, random=rand, back_url='/')

@login_routes.route('/register')
@login_routes.route('/createuser')
def get_create_user_page():
    rand = None
    app = utils.get_app()
    if app.debug != False:
        rand = random.random()

    template_name = 'create_user.html'

    # if utils.is_on_mobile(request.headers.get('User-Agent')):
    #     template_name = 'mobile/create_user.mobile.html'

    return render_template(template_name, random=rand, back_url='/')

@login_routes.route('/api/createuser', methods=['POST'])
def create_user():
    data = request.values
    if data is None or len(data)==0:
        data = request.get_json(force=True)

    email = data.get('email').lower()
    if email == "":
        email = None
    phone_number = data.get('phone')
    if phone_number == "":
        phone_number = None

    name = data.get('firstname')
    surname = data.get('lastname')
    password = data.get('password')

    if (email is None or email == "") and (phone_number is None or phone_number==""):
        return jsonify(status='fail', message='Email or phone number required')

    if len(email) > 200:
        return jsonify(stauts='fail', message='Email is too long (please use less than 200 characters)')

    if name is None or name == "":
        return jsonify(status='fail', message='Name cannot be blank')

    if password is None:
        return jsonify(status='fail', message='Password cannot be blank')

    if len(name) > 50:
        return jsonify(status='fail', message='Name cannot be longer than 50 characters')

    session = get_db_session()
    user = session.query(User).filter_by(email=email).first()

    if user is not None: 
        return jsonify(status='fail', message='User already exists')

    user = session.query(User).filter_by(phone_number=phone_number).first()

    if user is not None: 
        return jsonify(status='fail', message='User already exists')

    user = User(name, surname, phone_number, email)
    # def __init__(self, first_name, last_name, phone_number=None, email=None, password=None, salt=None):
    user.status = 'user'
    user.confirmed = 1

    user.salt = bcrypt.gensalt().decode()
    user.password = bcrypt.hashpw(password.encode(), user.salt.encode()).decode()    

    session.add(user)
    session.commit()

    return jsonify(status='ok')

@login_routes.route('/confirm/<string:conf_guid>', methods=['GET'])
def get_confirmation_page(conf_guid):
    rand = None
    if app.debug != False:
        rand = random.random()

    template_name = 'confirmation.html'

    if utils.is_on_mobile(request.headers.get('User-Agent')):
        template_name = 'mobile/confirmation.mobile.html'

    session = get_db_session()
    user = session.query(User).filter_by(confirmation_guid=conf_guid).first()

    if user is None:
        return render_template(template_name, random=rand, back_url='/', message="No user exists")
    
    if user.confirmed != 0:
        return render_template(template_name, random=rand, back_url='/', message="This confirmation code has already been used")
    
    return render_template(template_name, random=rand, back_url='/', message=None, confirmation_guid=conf_guid)

@login_routes.route('/api/confirm/<string:conf_guid>', methods=['POST'])
def post_confirmation(conf_guid):
    if conf_guid is None:
        return jsonify(status='fail', message='')

    session = get_db_session()
    user = session.query(User).filter_by(confirmation_guid=conf_guid).first()

    if user is None:
        return jsonify(status='fail', message='Unable to confirm, user not found')
    
    if user.confirmed != 0:
        return jsonify(status='fail', message='Confirmation already used')

    data = request.values
    if data is None or len(data)==0:
        data = request.get_json(force=True)

    password = data.get('password')
    
    if password is None or password == "":
        return jsonify(status='fail', message='Password cannot be blank')

    if len(password) < 10:
        return jsonify(status='fail', message='Password must be 10 characters or more')
    
    user.salt = bcrypt.gensalt().decode()
    user.password = bcrypt.hashpw(password.encode(), user.salt.encode()).decode()    

    displayname = data.get('displayname')

    user.displayname = displayname
    user.confirmation_guid = None
    user.confirmed = 1 
    session.add(user)
    session.commit()

    secret = utils.get_jwt_secret()
    jwttoken = jwt.encode({'username': user.email}, secret, algorithm='HS256')

    return jsonify(status='ok', token=jwttoken.decode())

@login_routes.route('/api/reset', methods=['POST'])
def reset_password():
    data = request.values
    if data is None or len(data)==0:
        data = request.get_json(force=True)

    email = data.get('email')
    if email is None:
        return jsonify(status='fail', message='Please provide an email address')

    session = get_db_session()
    user = session.query(User).filter_by(email=email).first()

    if user is None:
        return jsonify(status='fail', message='User not found')
    
    if user.confirmed == 0:
        return jsonify(status='fail', message='User not yet confirmed')
    
    # Generate reset guid
    guid = uuid.uuid4().hex
    user.confirmation_guid = guid
    session.add(user)
    session.commit()

    body = "Please go to https://electrocatstudios.com/resetpassword/{}".format(guid)
    text_body = "Please go to https://electrocatstudios.com/resetpassword/{}".format(guid)

    to = email
    sender = "phil@electrocatstudios.com"
    subject = "Reset Your Password"
    msgHtml = body
    msgPlain = text_body
    SendMessage(sender, to, subject, msgHtml, msgPlain)

    return jsonify(status='ok', message='Reset Email Sent')

@login_routes.route('/api/updatepassword', methods=['POST'])
def update_password():
    data = request.values
    if data is None or len(data)==0:
        data = request.get_json(force=True)

    email = data.get('email')
    if email is None:
        return jsonify(status='fail', message='Please provide an email address')

    reset_code = data.get('reset_code')
    if reset_code is None:
        return jsonify(status='fail', message='Unknown Error')

    password = data.get('password')
    if password is None or password=="":
        return jsonify(status='fail', message='Please provide an password address')
    
    session = get_db_session()
    user = session.query(User).filter_by(email=email).first()
    if user.confirmation_guid != reset_code:
        print(reset_code)
        print(user.confirmation_guid)
        return jsonify(status='fail', message='Incorrect email and reset code combination')
    
    # Check reset code against email
    user.password = bcrypt.hashpw(password.encode(), user.salt.encode()).decode()    
    session.add(user)
    session.commit()

    return jsonify(status='ok')    

@login_routes.route('/resetpassword/<string:resetguid>', methods=['GET'])
@login_routes.route('/passwordreset/<string:resetguid>', methods=['GET'])
def reset_page(resetguid):
    rand = None
    if app.debug != False:
        rand = random.random()

    template_name = 'reset.html'

    if utils.is_on_mobile(request.headers.get('User-Agent')):
        template_name = 'mobile/reset.mobile.html'
    error = ""
   
    session = get_db_session()
    user = session.query(User).filter_by(confirmation_guid=resetguid).first()

    if user is None:
        error = "Invalid confirmation code"

    return render_template(template_name, random=rand, back_url='/', error=error, reset_code=resetguid)