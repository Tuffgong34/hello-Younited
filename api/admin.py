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
from db.club import Club
from db.position import Position

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
    allowed_status = ['admin', 'sadmin']

    if user.status not in allowed_status:
        print("ERROR: unauthorized access of resource attempted")
        return jsonify(status='fail', message='unauthorized', authorized=False)

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

    clubs = session.query(Club).all()
    club_list = []
    for c in clubs:
        players = session.query(Player).filter_by(club_id=c.id).all()
        player_list = []
        for p in players:
            position = {
                "name": "center forward"
            }
            next_p = {
                "id": p.id,
                "first_name": p.first_name,
                "last_name": p.last_name,
                "shirt_number": p.shirt_number,
                "date_of_birth": p.date_of_birth,
                "height_cm": p.height_cm,
                "position":  position,
                "yn_user_id": p.yn_user_id,
                "created_at": p.created_at 
            }
            player_list.append(next_p)
        next_club = {
            "id": c.id,
            "name": c.name,
            "players": player_list,
            "founded": c.founded,
            "contact": c.contact,
            "location": c.location,
            "division_id": c.division_id,
            "created_at": c.created_at
        }
        club_list.append(next_club)
    positions = session.query(Position).all()
    pos_out = []
    for p in positions:
        next_pos = {
            "id": p.id,
            "name": p.name,
            "description": p.description
        }
        pos_out.append(next_pos)

    data_obj = {
        "firstname": user.first_name,
        "lastname": user.last_name,
        "usercount": usercount,
        "playercount": playercount,
        "leagues": league_data,
        "clubs": club_list,
        "positions": pos_out
    }
       
    return jsonify(status='ok', data=data_obj)

@utils.check_auth_admin
@admin_api_routes.route('/api/league', methods=['POST'])
def post_league():
    user = utils.get_user(request)
    allowed_status = ['admin', 'sadmin']

    if user.status not in allowed_status:
        print("ERROR: unauthorized access of resource attempted")
        return jsonify(status='fail', message='unauthorized', authorized=False)

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
        dt_founded = datetime.datetime.strptime(founded, '%Y-%m-%d')
        print(dt_founded)
        league.founded = dt_founded

    session.add(league)
    session.commit()
    return jsonify(status='ok')

@utils.check_auth_admin
@admin_api_routes.route('/api/division', methods=['POST'])
def post_division():
    user = utils.get_user(request)
    allowed_status = ['admin', 'sadmin']

    if user.status not in allowed_status:
        print("ERROR: unauthorized access of resource attempted")
        return jsonify(status='fail', message='unauthorized', authorized=False)

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

@utils.check_auth_admin
@admin_api_routes.route('/api/club', methods=['POST'])
def post_club():
    user = utils.get_user(request)
    allowed_status = ['admin', 'sadmin']

    if user.status not in allowed_status:
        print("ERROR: unauthorized access of resource attempted")
        return jsonify(status='fail', message='unauthorized', authorized=False)

    data = request.values
    if data is None or len(data)==0:
        data = request.get_json(force=True)
    if data is None:
        return jsonify(status='fail', message='message body was blank')
    name = data['name']
    if name is None or name == "":
        return jsonify(status='fail', message='name cannot be blank')

    information = data['information']
    location = data['location']
    founded = data['founded']
    contact = data['contact']
    division = data['division']
    try:
        division = int(division)
    except:
        return jsonify(status='fail', message='division value is not valid')

    session = get_db_session()
    club = Club(name, division)
    
    if information is not None and information != "":
        club.information = information
    if location is not None and location != "":
        club.location = location
    if founded is not None and founded != "":
        dt_founded = datetime_object = datetime.datetime.strptime(founded, '%Y-%m-%d')
        print(dt_founded)
        club.founded = dt_founded
    if contact is not None and contact != "":
        club.contact = contact
    
    session.add(club)
    session.commit()
    return jsonify(status='ok')

@utils.check_auth_admin
@admin_api_routes.route('/api/player', methods=['POST'])
def post_player():
    user = utils.get_user(request)
    allowed_status = ['admin', 'sadmin']

    if user.status not in allowed_status:
        print("ERROR: unauthorized access of resource attempted")
        return jsonify(status='fail', message='unauthorized', authorized=False)

    data = request.values
    if data is None or len(data)==0:
        data = request.get_json(force=True)
    if data is None:
        return jsonify(status='fail', message='message body was blank')

    name = data['last_name']
    if name is None or name == "":
        return jsonify(status='fail', message='last name cannot be blank')

    first_name = data['first_name']
    shirt_number = data['shirt_number']
    if shirt_number is not None and shirt_number != "":
        try:
            shirt_number = int(shirt_number)
        except:
            return jsonify(status='fail', message='shirt number must be a number')
    
    date_of_birth = data['date_of_birth']
    try:
        if date_of_birth is not None and date_of_birth!="":
            date_of_birth = datetime.datetime.strptime(date_of_birth, '%Y-%m-%d')
    except:
        return jsonify(status='fail', message='date of birth invalid')

    height_cm = data['height_cm']
    if height_cm is not None and height_cm != "":
        try:
            height_cm = int(height_cm)
        except:
            return jsonify(status='fail', message='height must be a number')
    
    club_id = data['club']
    if club_id is not None and club_id != "":
        try:
            club_id = int(club_id)
        except:
            return jsonify(status='fail', message='club id is invalid')

    position_id = data['position_id']
    if position_id is not None and position_id != "":
        try:
            position_id = int(position_id)
        except:
            return jsonify(status='fail', message='position id must be a number')

    shirt_color = data['shirt_color']
    yn_user_id = data['user_id']
    if yn_user_id is not None and yn_user_id != "":
        try:
            yn_user_id = int(yn_user_id)
        except:
            return jsonify(status='fail', messasge='user id is not valid')
    
    player = Player(name, club_id)
    if first_name is not None and first_name != "":
        player.first_name = first_name
    if shirt_number is not None:
        player.shirt_number = shirt_number
    if date_of_birth is not None:
        player.date_of_birth = date_of_birth
    if height_cm is not None:
        player.height_cm = height_cm
    if position_id is not None:
        player.position_id = position_id
    if shirt_color is not None and shirt_color != "":
        player.shirt_color = shirt_color
    if yn_user_id is not None and yn_user_id != "":
        player.yn_user_id = yn_user_id

    session = get_db_session()
    session.add(player)
    session.commit()
    return jsonify(status='ok')