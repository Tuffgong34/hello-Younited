import os
import json 
import jwt 
from flask import request
from utils.dbutils import get_db_session
from db.user import User

global_app = None
global_secret = None

def set_app(app):
    global global_app

    if global_app is not None:
        print("we are setting up app again")

    global_app = app

def get_app():
    global global_app

    if global_app is None:
        print("we are getting the global app before it's set")

    return global_app

def is_on_mobile(useragent):
    platforms = ["android", "ipad", "iphone"]
    if useragent is None:
        return False
        
    if any(platform in useragent.lower() for platform in platforms):
    # if any(platforms) in useragent:
        return True
    return False

def is_on_iphone(useragent):
    platforms = ["iphone"]
    if any(platform in useragent.lower() for platform in platforms):
    # if any(platforms) in useragent:
        return True
    return False

def get_jwt_secret():
    global global_secret

    if global_secret is None:
        with open('creds.json') as json_data:
                d = json.loads(json_data.read())
                global_secret = d['secret']

    return global_secret

def decode_jwt_token(token):
    secret = get_jwt_secret()
    return jwt.decode(token, secret, algorithms=['HS256'])

def get_user(request):
    key = request.headers.get('Authorization')
    if key is None:
        return jsonify(status='fail', message='no token provided')
    
    token = key.split(" ")[1]
    if token is None:
        return jsonify(status='fail', message='failed token check')
    
    decode = decode_jwt_token(token)

    if decode['username'] is None:
        return jsonify(status='fail', message='failed token check')
    username = decode['username']

    allowed_status = ['admin', 'sadmin']

    session = get_db_session()
    user = session.query(User).filter_by(email=username).first()
    if user is None:
        user = session.query(User).filter_by(phone_number=username).first()
    
    return user     

def check_auth_admin(func):
    def wrapper():
        user = get_user(request)
        
        if user is None:
            return jsonify(status='fail', message='user does not exist')
        
        if not isinstance(user, User):
            # user is a jsonified error
            return user

        session = get_db_session()

        if user.status not in allowed_status:
            print("ERROR: Attempt to use disabled account (id:{} - name:{} - status: {})".format(user.id, user.name, user.status))
            return jsonify(status='fail', message='unauthorized')
        
        func()

    return wrapper
