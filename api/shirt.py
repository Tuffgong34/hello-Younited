import jwt

from flask import jsonify, Blueprint, request, render_template
import json
from utils.dbutils import get_db_session
import utils.utils as utils
import bcrypt
from db.user import User
from db.shirt import Shirt
import random 
import smtplib 

import httplib2
import os
import base64

import uuid

shirt_api_routes = Blueprint('shirt_api_routes', __name__)

@shirt_api_routes.route('/api/shirt/<int:shirt_id>', methods=['GET'])
def get_shirt_data(shirt_id):
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

    shirt = session.query(Shirt).filter_by(phone_number=username).first()
    if shirt is None:
        return jsonify(status='fail', message='shirt does not exist')

    data_obj = {
        "style": shirt.style,
        "primary_color": shirt.primary_color,
        "secondary_color": shirt.secondary_color
    }

    return jsonify(status='ok', data=data_obj)

@shirt_api_routes.route('/api/shirt', methods=['GET'])
def get_all_shirt_data():
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

    shirts = session.query(Shirt).all()
    
    shirts_list = []
    for shirt in shirts:
        next_shirt = {
            "id": shirt.id,
            "style": shirt.style,
            "primary_color": shirt.primary_color,
            "secondary_color": shirt.secondary_color
        }
        shirts_list.append(next_shirt)

    data_obj = {
        "shirts": shirts_list
    }

    return jsonify(status='ok', data=data_obj)

@shirt_api_routes.route('/api/shirt', methods=['POST'])
def post_shirt():
    data = request.values
    if data is None or len(data)==0:
        data = request.get_json(force=True)

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
    
    style = data['style']
    if style is None or style == "":
        return jsonify(status='fail', message='must provide a style')
    
    primary = data['primary_color']
    if primary is None or primary == "":
        return jsonfiy(status='fail', message='primary color cannot be none')

    secondary = data['secondary_color']

    shirt = Shirt(style, primary)
    if secondary != "":
        shirt.secondary_color = secondary

    session.add(shirt)
    session.commit()

    return jsonify(status='ok', shirt_id=shirt.id)