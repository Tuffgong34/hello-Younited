# functions for creating and updating the matches on the system
import jwt

from flask import jsonify, Blueprint, request, render_template
import json

from db.match import Match
from db.user import User
from db.club import Club 
from db.event import Event
from db.player import Player
from db.event_type import EventType
from db.shirt import Shirt

import utils.utils as utils
from utils.dbutils import get_db_session

match_api_routes = Blueprint('match_api_routes', __name__)

@match_api_routes.route('/api/matches', methods=['GET'])
def get_matches():
    # Get the most recent matches
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
    
    matches = session.query(Match).order_by(Match.played)
    data = {
        'matches': []
    }
    for match in matches:
        home_club = session.query(Club).filter_by(id=match.home_club_id).first()
        away_club = session.query(Club).filter_by(id=match.away_club_id).first()
        if home_club is not None and away_club is not None:
            next_match = {
                'id': match.id,
                'home_club': home_club.name,
                'away_club': away_club.name,
                'played_at': match.played 
            }
            data['matches'].append(next_match) 
        else:
            print("ERROR: Match (id: {}) is missing home club ({}) or away club ({})".format(
                match.id,
                match.home_club_id,
                match.away_club_id
            ))
    return jsonify(status='ok', data=data)

@match_api_routes.route('/api/match/<int:matchid>', methods=['GET'])
def get_match_by_id(matchid):
    # Get the most recent matches
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
    
    match = session.query(Match).filter_by(id=matchid).first()
    if match is None:
        return jsonify(status='fail', message='match does not exist')
    if match.home_club_id is None:
        return jsonify(status='fail', message='home club is blank')
    if match.away_club_id is None:
        return jsonify(status='fail', message='away club is blank')
    
    home_club = session.query(Club).filter_by(id=match.home_club_id).first()
    if home_club is None:
        return jsonify(status='fail', message='Home club does not exist')
        
    away_club = session.query(Club).filter_by(id=match.away_club_id).first()
    if away_club is None:
        return jsonify(status='fail', message='Away club does not exist')
    
    
    home_club_data = {
        'name': home_club.name,
        'goals': [],
        'logo': home_club.logo_filename       
    }
    away_club_data = {
        'name': away_club.name,
        'goals': [],
        'logo': away_club.logo_filename
    }

    events = session.query(Event).filter_by(match_id=matchid).order_by(Event.occurred_at).all()
    other_events = []
    for event in events:
        if event.event_type_id == 1:
            player = session.query(Player).filter_by(id=event.player_1_id).first()
            if player is None:
                return jsonify(status='fail', message="Failed to find player {}".format(event.player_1_id))
            club = session.query(Club).filter_by(id=player.club_id).first()
            if club is None:
                return jsonify(status='fail', message='Failed to find club {}'.format(player.club_id))
            shirt = {}
            if club.home_shirt_id is not None:
                shirt = utils.get_shirt_for_id(session, club.home_shirt_id)
            club_info = {
                'name': club.name,
                'shirt': shirt,
                'club': club.logo_filename
            }
            
            next_goal = {
                'type': 'Goal',
                'scorer': "{} {}".format(player.first_name, player.last_name),
                'scorer_id': player.id,
                'time': event.occurred_at,
                'support': None,
                'support_id': None,
                'club': club_info
            }
            if event.player_2_id is not None:
                support = session.query(Player).filter_by(id=event.player_2_id).first()
                next_goal['support'] = "{} {}".format(support.first_name, support.last_name)
                next_goal['support_id'] = support.id

            if player.club_id == home_club.id:
                home_club_data['goals'].append(next_goal)
            elif player.club_id == away_club.id:
                away_club_data['goals'].append(next_goal)
            else:
                return jsonify(status='fail', message='Failed to fit player to team')
        else:
            # TODO: Add in shirt details for front end
            p1 = None
            club_data = None
            if event.player_1_id is not None:
                playr = session.query(Player).filter_by(id=event.player_1_id).first()
                if playr is None:
                    return jsonify(status='fail', message='Failed to find player')
                p1 = {
                    'id': playr.id,
                    'name': "{} {}".format(playr.first_name, playr.last_name)
                }
                club = session.query(Club).filter_by(id=playr.club_id).first()
                if club is not None:
                    shirt = {}
                    if club.home_shirt_id is not None:
                        shirt = utils.get_shirt_for_id(session, club.home_shirt_id)
                    club_data = {
                        'name': club.name,
                        'shirt': shirt,
                        'logo': club.logo_filename
                    }

            p2 = None
            if event.player_2_id is not None:
                playr = session.query(Player).filter_by(id=event.player_2_id).first()
                if playr is None:
                    return jsonify(status='fail', message='Failed to find player')
                p2 = {
                    'id': playr.id,
                    'name': "{} {}".format(playr.first_name, playr.last_name)
                }
            
            next_event = {
                'type': utils.get_name_of_event(session, event.event_type_id),
                'time': event.occurred_at,
                'player': p1,
                'club': club_data,
                'other_player': p2,
                'information': event.information
            }
            other_events.append(next_event)
    data = {
        'home_club': home_club_data,
        'away_club': away_club_data,
        'events': other_events
    }

    return jsonify(status='ok', data=data)

@utils.check_auth_admin
@match_api_routes.route('/api/match', methods=['POST'])
def post_match():
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

    home_club_id = data['home_club_id']
    away_club_id = data['away_club_id']
    played_date = data['played_date']
    match = Match()
    return jsonify(status='ok')
