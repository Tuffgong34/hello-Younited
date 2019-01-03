import jwt
from flask import jsonify, Blueprint, request, render_template
import json
from utils.dbutils import get_db_session
import utils.utils as utils
from db.user import User

import random 
import smtplib 

import httplib2
import os

club_page_routes = Blueprint('club_page_routes', __name__)

@club_page_routes.route('/club/<int:club_id>', methods=['GET'])
def get_club_page(club_id):
    rand = None
    app = utils.get_app()
    if app.debug != False:
        rand = random.random()

    template_name = 'club.html'

    # if utils.is_on_mobile(request.headers.get('User-Agent')):
    #     template_name = 'mobile/create_user.mobile.html'

    return render_template(template_name, random=rand, back_url='/', club_id=club_id)


@club_page_routes.route('/player/<int:player_id>', methods=['GET'])
def get_player_page(player_id):
    rand = None
    app = utils.get_app()
    if app.debug != False:
        rand = random.random()

    template_name = 'player.html'

    # if utils.is_on_mobile(request.headers.get('User-Agent')):
    #     template_name = 'mobile/create_user.mobile.html'

    return render_template(template_name, random=rand, back_url='/', player_id=player_id)
