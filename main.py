from flask import Flask, jsonify, render_template, send_file, request, Markup, abort, make_response, Response
import sys
import random
from os.path import isfile, join

from api.login import login_routes
from api.profile import profile_api_routes
from api.admin import admin_api_routes
from api.league import league_api_routes
from api.club import club_api_routes

import utils.utils as utils

from pages.profile import profile_page_routes
from pages.admin import admin_page_routes
from pages.leagues import league_page_routes
from pages.club import club_page_routes

app = Flask(__name__)
utils.set_app(app)
app.register_blueprint(login_routes)

app.register_blueprint(profile_api_routes)
app.register_blueprint(admin_api_routes)
app.register_blueprint(league_api_routes)
app.register_blueprint(club_api_routes)

app.register_blueprint(admin_page_routes)
app.register_blueprint(league_page_routes)
app.register_blueprint(profile_page_routes)
app.register_blueprint(club_page_routes)

@app.route('/')
@app.route('/index.html')
@app.route('/index')
def index_page():
    rand = None
    if app.debug != False:
        rand = random.random()

    template_name = 'index.html'
    # if utils.is_on_mobile(request.headers.get('User-Agent')):
    #     template_name = 'mobile/index.mobile.html'

    # image_list = "['/img/front_page_banner/logo.png','/img/front_page_banner/rpi_wires.png']"
    return render_template(template_name, debug=app.debug, random=rand)

@app.route('/css/<path:path>')
def css_get(path):
    fn = 'assets/css/' + path
    if not isfile(fn):
        return render_template('404.html'), 404
    return send_file(fn)

@app.route('/js/<path:path>')
def js_get(path):
    fn = 'assets/js/' + path
    if not isfile(fn):
        return render_template('404.html'), 404
    return send_file(fn)

if __name__ == '__main__':
    debug = False

    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        debug = True

    app.run(host='0.0.0.0',debug=debug)
