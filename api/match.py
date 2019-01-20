# functions for creating and updating the matches on the system
import jwt

from flask import jsonify, Blueprint, request, render_template
import json

from db.match import Match
from db.user import User

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




def update_results_cache():
    # Update the results cache and league standing
    pass

