import jwt
from flask import jsonify, Blueprint, request, render_template
import json
import utils.utils as utils
import random 
import smtplib 

import httplib2
import os

match_page_routes = Blueprint('match_page_routes', __name__)

@match_page_routes.route('/match', methods=['GET'])
def get_matches_page():
    rand = None
    app = utils.get_app()
    if app.debug != False:
        rand = random.random()

    template_name = 'match.html'

    # if utils.is_on_mobile(request.headers.get('User-Agent')):
    #     template_name = 'mobile/create_user.mobile.html'

    return render_template(template_name, random=rand, back_url='/', league_id=None)

@match_page_routes.route('/match/<int:matchid>', methods=['GET'])
def get_match_page_by_id(matchid):
    rand = None
    app = utils.get_app()
    if app.debug != False:
        rand = random.random()

    template_name = 'match_detail.html'

    # if utils.is_on_mobile(request.headers.get('User-Agent')):
    #     template_name = 'mobile/create_user.mobile.html'

    return render_template(template_name, random=rand, back_url='/', league_id=None, matchid=matchid)