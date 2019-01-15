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
from db.shirt import Shirt
from db.match import Match
from db.result_cache import ResultCache

import random 
import smtplib 

import httplib2
import os
import base64

import uuid

league_api_routes = Blueprint('league_api_routes', __name__)

@league_api_routes.route('/api/leagues', methods=['GET'])
def get_all_leagues_data():
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
    leagues = session.query(League).all()
    league_out = []
    for l in leagues:
        next_league = {
            "id": l.id,
            "name": l.name,
            "description": l.description,
            "location": l.location
        }
        league_out.append(next_league)
    data_obj = {
        "leagues": league_out
    }
       
    return jsonify(status='ok', data=data_obj)

@league_api_routes.route('/api/league/<int:league_id>', methods=['GET'])
def get_league_data(league_id):
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
    league = session.query(League).filter_by(id=league_id).first()
    if league is None:
        return jsonify(status='fail', message='league does not exist')

    divisions = session.query(Division).filter_by(league_id=league.id).all()
    
    div_out = []
    for d in divisions:
        next_div = {
            "id": d.id,
            "name": d.name,
            "description": d.description,
            "location": d.location,
            "founded": d.founded
        }
        div_out.append(next_div)
    league_out = {
        "name": league.name,
        "description": league.description,
        "founded": league.founded,
        "location": league.location
    }
    data_obj = {
        "league": league_out,
        "divisions": div_out
    }
       
    return jsonify(status='ok', data=data_obj)

@league_api_routes.route('/api/division/<int:div_id>', methods=['GET'])
def get_division_data(div_id):
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
    
    division = session.query(Division).filter_by(id=div_id).first()
    if division is None:
        return jsonify(status='fail', message='division does not exist')

    clubs = session.query(Club).filter_by(division_id=div_id).all()

    clubs_out = []
    for c in clubs:
        rc = session.query(ResultCache).filter_by(competition_id=division.display_competition_id).filter_by(club_id=c.id).first()
        if rc is None:
            next_rc = {
                "win": 0,
                "loss": 0,
                "draw": 0,
                "points": 0,
                "goals_against": 0,
                "goals_for": 0,
                "goal_difference": 0
            }
        else:
            next_rc = {
                "win": rc.win,
                "loss": rc.loss,
                "draw": rc.draw,
                "points": rc.points,
                "goals_against": rc.goals_against,
                "goals_for": rc.goals_for,
                "goal_difference": rc.goal_difference
            }

        next_club = {
            "id": c.id,
            "name": c.name,
            "contact": c.contact,
            "location": c.location,
            "founded": c.founded,
            "information": c.information,
            "rc": next_rc
        }
        # home_matches = session.query(Match).filter_by(home_club_id)
        if c.home_shirt_id is not None:
            shirt = session.query(Shirt).filter_by(id=c.home_shirt_id).first()
            if shirt is not None:
                next_shirt = {
                    "style": shirt.style,
                    "primary_color": shirt.primary_color,
                    "secondary_color": shirt.secondary_color
                }
                next_club['home_shirt'] = next_shirt
        
        if c.goalkeeper_shirt_id is not None:
            shirt = session.query(Shirt).filter_by(id=c.goalkeeper_shirt_id).first()
            if shirt is not None:
                next_shirt = {
                    "style": shirt.style,
                    "primary_color": shirt.primary_color,
                    "secondary_color": shirt.secondary_color
                }
                next_club['goalkeeper_shirt'] = next_shirt
                
        clubs_out.append(next_club)
    division_out = {
        "name": division.name,
        "description": division.description,
        "founded": division.founded,
        "location": division.location
    }
    data_obj = {
        "division": division_out,
        "clubs": clubs_out
    }
       
    return jsonify(status='ok', data=data_obj)