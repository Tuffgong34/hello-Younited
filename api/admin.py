import jwt

from flask import jsonify, Blueprint, request, render_template
import json
from utils.dbutils import get_db_session
import utils.utils as utils
import bcrypt

from db.user import User
from db.player import Player
from db.league import League
from db.division import Division

import random 
import smtplib 

import httplib2
import os
import base64
from sqlalchemy import func
import uuid
import datetime 

admin_api_routes = Blueprint('admin_api_routes', __name__)

@utils.check_auth_admin
@admin_api_routes.route('/api/admin', methods=['GET'])
def get_admin_details():
    user = utils.get_user(request)
    session = get_db_session()
    usercount = session.query(func.count(User.id)).scalar()
    playercount = session.query(func.count(Player.id)).scalar()
    leagues = session.query(League).all()
    league_data = []
    for l in leagues:
        divisions = session.query(Division).filter_by(league_id=l.id).all()
        div_details = []
        for d in divisions:
            next_d = {
                "id": d.id,
                "name": d.name,
                "description": d.description,
                "location": d.location,
                "founded": d.founded
            }
            div_details.append(next_d)

        next_l = {
            "id": l.id,
            "name": l.name,
            "description": l.description,
            "location": l.location,
            "founded": l.founded,
            "divisions": div_details
        }
        league_data.append(next_l)

    data_obj = {
        "firstname": user.first_name,
        "lastname": user.last_name,
        "usercount": usercount,
        "playercount": playercount,
        "leagues": league_data
    }
       
    return jsonify(status='ok', data=data_obj)

@utils.check_auth_admin
@admin_api_routes.route('/api/league', methods=['POST'])
def post_league():
    user = utils.get_user(request)
    
    data = request.values
    if data is None or len(data)==0:
        data = request.get_json(force=True)
    if data is None:
        return jsonify(status='fail', message='message body was blank')
    name = data['name']
    if name is None or name == "":
        return jsonify(status='fail', message='name cannot be blank')

    description = data['description']
    location = data['location']
    founded = data['founded']

    session = get_db_session()
    league = League(name)
    if description is not None and description != "":
        league.description = description
    if location is not None and location != "":
        league.location = location
    if founded is not None and founded != "":
        dt_founded = datetime_object = datetime.datetime.strptime(founded, '%Y-%m-%d')
        print(dt_founded)
        league.founded = dt_founded

    session.add(league)
    session.commit()
    return jsonify(status='ok')

@utils.check_auth_admin
@admin_api_routes.route('/api/division', methods=['POST'])
def post_division():
    user = utils.get_user(request)
    
    data = request.values
    if data is None or len(data)==0:
        data = request.get_json(force=True)
    if data is None:
        return jsonify(status='fail', message='message body was blank')
    name = data['name']
    if name is None or name == "":
        return jsonify(status='fail', message='name cannot be blank')

    description = data['description']
    location = data['location']
    founded = data['founded']
    league = data['league']
    try:
        league = int(league)
    except:
        return jsonify(status='fail', message='league value is not valid')

    session = get_db_session()
    division = Division(name, league)
    
    if description is not None and description != "":
        division.description = description
    if location is not None and location != "":
        division.location = location
    if founded is not None and founded != "":
        dt_founded = datetime_object = datetime.datetime.strptime(founded, '%Y-%m-%d')
        print(dt_founded)
        division.founded = dt_founded
    
    session.add(division)
    session.commit()
    return jsonify(status='ok')