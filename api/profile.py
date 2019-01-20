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

profile_api_routes = Blueprint('profile_api_routes', __name__)

@profile_api_routes.route('/api/profile', methods=['GET'])
def get_profile_data():
    key = request.headers.get('Authorization')
    if key is None:
        return jsonify(status='fail', message='no token provided')
    
    token = key.split(" ")[1]
    if token is None:
        return jsonify(status='fail', message='failed token check')
    
    decode = utils.decode_jwt_token(token)

    if decode['username'] is None:
        return jsonify(status='fail', message='failed token check')
    username = decode['username']
  
    allowed_status = ['user', 'admin', 'sadmin']

    session = get_db_session()
    user = session.query(User).filter_by(email=username).first()
    if user is None:
        user = session.query(User).filter_by(phone_number=username).first()
 
    if user is None:
        return jsonify(status='fail', message='user does not exist')
    
    if user.status not in allowed_status:
        print("ERROR: Attempt to use disabled account (id:{} - name:{} - status: {})".format(user.id, user.name, user.status))
        return jsonify(status='fail', message='account has been disabled')
    # TODO: Add in standard menu items 
    menu_items = [
        {
            "name": "Profile",
            "link": "/profile"
        },
        {
            "name": "Leagues",
            "link": "/league"
        }
    ]
    if user.status == "sadmin":
        menu_items.append({
            "name": "Admin Page",
            "link": "/admin"
        })
        menu_items.append({
            "name": "Shirt Design",
            "link": "/admin/shirt"
        })
    
    menu_items.append({
        "name": "Matches",
        "link": "/match"
    })
    

    # Logout should be last
    menu_items.append({
        "name": "Log out",
        "link": "/logout"
    })
    
    data_obj = {
        "firstname": user.first_name,
        "lastname": user.last_name,
        "menu_items": menu_items 
    }
       
    return jsonify(status='ok', data=data_obj)
