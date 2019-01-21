import os
import json 
import jwt 
from flask import request
from utils.dbutils import get_db_session
from db.user import User
from db.match import Match
from db.event import Event
from db.event_type import EventType
from db.player import Player

from sqlalchemy import or_

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


    session = get_db_session()
    user = session.query(User).filter_by(email=username).first()
    if user is None:
        user = session.query(User).filter_by(phone_number=username).first()
    
    return user     

def check_auth_admin(func):
    def wrapper():
        user = get_user(request)

        allowed_status = ['admin', 'sadmin']

        if user.status not in allowed_status:
            print("ERROR: unauthorized access of resource attempted")
            return jsonify(status='fail', message='unauthorized', authorized=False)

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

def get_name_of_event(session, event_id):
    ev = session.query(EventType).filter_by(id=event_id).first()
    if ev is None:
        print("Unknown id for event {}".format(event_id))
        return "Unknown"
    return ev.name

def get_shirt_for_id(session, home_shirt_id):
    shirt = session.query(Shirt).filter_by(id=home_shirt_id).first()
    if shirt is None:
        return {}
    shirt_val = {
        'id': shirt.id,
        'style': shirt.style,
        'primary_color': shirt.primary_color,
        'secondary_color': shirt.secondary_color
    }
    return shirt_val


def get_match_data(session, club_id):
    # Get the last 10 matches for the given club id
    matches = session.query(Match).filter(or_(Match.home_club_id==club_id, Match.away_club_id==club_id)) 
    #.order_by(Match.played)
    return matches

def get_player_info(session, player_id):
    if player_id is None:
        return None
    player = session.query(Player).filter_by(id=player_id).first()
    if player is None:
        print("ERROR: player {} not found".format(player_id))
        return None
    retval = {
        'name': "{} {}".format(player.first_name, player.last_name),
        'shirt_number': player.shirt_number,
        'id': player.id,
        'club_id': player.club_id
    }
    return retval

def get_all_events(session, match_id):
    events = session.query(Event).filter_by(match_id=match_id).all()
    retval = []
    for ev in events:
        t = get_name_of_event(session, ev.event_type_id)
        next_ev = {
            'type': t,
            'occurred_at': ev.occurred_at,
            'player_1': get_player_info(session, ev.player_1_id),
            'player_2': get_player_info(session, ev.player_2_id),
            'information': ev.information
        }
        retval.append(next_ev)
    return retval