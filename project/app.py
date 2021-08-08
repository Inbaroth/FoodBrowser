import json
import os

from flask import Blueprint, url_for
from flask import jsonify, request, redirect, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)


@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.favorites'))
    return redirect(url_for('auth.login'))


@main.route('/favorites')
@login_required
def favorites():
    return render_template('favorites.html', name=current_user.username)


@main.route('/mainsearch')
@login_required
def foodSearch():
    return render_template('foodSearch.html', name=current_user.username)


@main.route('/foodsearch')
@login_required
def mainSearch():
    return render_template('autocomplete.html')


# TODO: currently has the ability to get requests from UI while typing
# TODO: instead of searching in a in-memory json file, should have asyncs requests to external API
# TODO: responses should be both text & images
@main.route('/search', methods=['GET', 'POST'])
def search():
    term = request.form['q']
    print('term: ', term)

    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "data", "results.json")
    json_data = json.loads(open(json_url).read())

    filtered_dict = [v for v in json_data if term in v]
    print(filtered_dict)

    resp = jsonify(filtered_dict)
    # CORS handling
    resp.headers.add('Access-Control-Allow-Origin', '*')
    resp.status_code = 200
    return resp