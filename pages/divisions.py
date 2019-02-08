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

division_page_routes = Blueprint('division_page_routes', __name__)

@division_page_routes.route('/divisions', methods=['GET'])
@division_page_routes.route('/division', methods=['GET'])
def get_divisions_page():
    rand = None
    app = utils.get_app()
    if app.debug != False:
        rand = random.random()

    template_name = 'division_list.html'

    # if utils.is_on_mobile(request.headers.get('User-Agent')):
    #     template_name = 'mobile/create_user.mobile.html'

    return render_template(template_name, random=rand, back_url='/', league_id=None)

