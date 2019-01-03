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

league_page_routes = Blueprint('league_page_routes', __name__)

@league_page_routes.route('/leagues', methods=['GET'])
@league_page_routes.route('/league', methods=['GET'])
def get_leagues_page():
    rand = None
    app = utils.get_app()
    if app.debug != False:
        rand = random.random()

    template_name = 'league.html'

    # if utils.is_on_mobile(request.headers.get('User-Agent')):
    #     template_name = 'mobile/create_user.mobile.html'

    return render_template(template_name, random=rand, back_url='/', league_id=None)

@league_page_routes.route('/league/<int:league_id>', methods=['GET'])
def get_leauge_page(league_id):
    rand = None
    app = utils.get_app()
    if app.debug != False:
        rand = random.random()

    template_name = 'league.html'

    # if utils.is_on_mobile(request.headers.get('User-Agent')):
    #     template_name = 'mobile/create_user.mobile.html'

    return render_template(template_name, random=rand, back_url='/', league_id=league_id)


@league_page_routes.route('/division/<int:div_id>', methods=['GET'])
def get_division_page(div_id):
    rand = None
    app = utils.get_app()
    if app.debug != False:
        rand = random.random()

    template_name = 'division.html'

    # if utils.is_on_mobile(request.headers.get('User-Agent')):
    #     template_name = 'mobile/create_user.mobile.html'

    return render_template(template_name, random=rand, back_url='/', div_id=div_id)
