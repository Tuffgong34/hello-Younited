import jwt

from flask import jsonify, Blueprint, request, render_template
import json
from utils.dbutils import get_db_session
import utils.utils as utils
import bcrypt
from db.user import User
from db.league import League
from db.club import Club
from db.division import Division
from db.player import Player
from db.position import Position
from db.shirt import Shirt

import random 
import smtplib 

import httplib2
import os
import base64

import uuid

club_api_routes = Blueprint('club_api_routes', __name__)

@club_api_routes.route('/api/club/<int:club_id>', methods=['GET'])
def get_club_data(club_id):
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
    
    club = session.query(Club).filter_by(id=club_id).first()
    if club is None:
        return jsonify(status='fail', message='club does not exist')

    players = session.query(Player).filter_by(club_id=club_id).all()

    club_out = {
        "name": club.name,
        "information": club.information,
        "founded": club.founded,
        "contact": club.contact,
        "home_shirt": None,
        "away_shirt": None,
        "goalkeeper_shirt": None
    }
    if club.home_shirt_id is not None:
        shirt = session.query(Shirt).filter_by(id=club.home_shirt_id).first()
        if shirt is None:
            print("ERROR: Unknown home_shirt_id {} for club_id {}".format(club.home_shirt_id, club.id))
        else:
            home_shirt = {
                "style": shirt.style,
                "primary_color": shirt.primary_color,
                "secondary_color": shirt.secondary_color
            }
            club_out['home_shirt'] = home_shirt

    if club.away_shirt_id is not None:
        shirt = session.query(Shirt).filter_by(id=club.away_shirt_id).first()
        if shirt is None:
            print("ERROR: Unknown away_shirt_id {} for club_id {}".format(club.away_shirt_id, club.id))
        else:
            away_shirt = {
                "style": shirt.style,
                "primary_color": shirt.primary_color,
                "secondary_color": shirt.secondary_color
            }
            club_out['away_shirt'] = away_shirt

    if club.goalkeeper_shirt_id is not None:
        shirt = session.query(Shirt).filter_by(id=club.goalkeeper_shirt_id).first()
        if shirt is None:
            print("ERROR: Unknown goalkeeper_shirt_id {} for club_id {}".format(club.goalkeeper_shirt_id, club.id))
        else:
            goalkeeper_shirt = {
                "style": shirt.style,
                "primary_color": shirt.primary_color,
                "secondary_color": shirt.secondary_color
            }
            club_out['goalkeeper_shirt'] = goalkeeper_shirt

    players_out = []
    for p in players:
        position = session.query(Position).filter_by(id=p.position_id).first()
        next_position = {}
        if position is not None:
            next_position["name"] = position.name
        else:
            pass
            # print("Player without position {}".format(p.id))
        next_player = {
            "id": p.id,
            "first_name": p.first_name,
            "last_name": p.last_name,
            "position": next_position
        }
        players_out.append(next_player)
    data_obj = {
        "club": club_out,
        "players": players_out
    }
       
    return jsonify(status='ok', data=data_obj)


@club_api_routes.route('/api/player/<int:player_id>', methods=['GET'])
def get_player_data(player_id):
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

    player = session.query(Player).filter_by(id=player_id).first()
    if player is None:
        return jsonify(status='fail', message='player does not exist')
    
    position = session.query(Position).filter_by(id=player.position_id).first()
    if position is None:
        pass
        # print("Player without position {}".format(player.id))
    
    club = session.query(Club).filter_by(id=player.club_id).first()

    club_out = {
        "name": "",
        "id": None
    }
    if club is not None:
        club_out["name"] = club.name
        club_out["id"] = club.id

    player_out = {
        "id": player.id,
        "first_name": player.first_name,
        "last_name": player.last_name,
        "shirt_number": player.shirt_number,
        "date_of_birth": player.date_of_birth,
        "height": player.height_cm,
        "home_shirt": {
            "style": "",
            "primary_color": "",
            "secondary_color": "",
        },
        "away_shirt": {
            "style": "",
            "primary_color": "",
            "secondary_color": "",
        },
        "goalkeeper_shirt": {
            "style": "",
            "primary_color": "",
            "secondary_color": ""
        },
        # "shirt_color": player.shirt_color,
        "claimed": False,
        "club": club_out
    }

    if position is not None:
        player_out["position"] = position.name
    if player.yn_user_id is None:
        player_out["claimed"] = True

    data_obj = {
        "player": player_out
    }
       
    return jsonify(status='ok', data=data_obj)