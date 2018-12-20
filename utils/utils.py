import os
import json 
import jwt 

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
