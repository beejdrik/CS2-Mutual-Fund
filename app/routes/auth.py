from flask import Blueprint, redirect, url_for, session, request
from flask_login import login_user, logout_user, login_required
from app import db
from app.models import User
import requests
import re

auth = Blueprint('auth', __name__)

STEAM_OPENID_URL = 'https://steamcommunity.com/openid/login'

@auth.route('/login')
def login():
    params = {
        'openid.ns': 'http://specs.openid.net/auth/2.0',
        'openid.mode': 'checkid_setup',
        'openid.return_to': url_for('auth.authorized', _external=True),
        'openid.realm': 'http://localhost:5000/',                  #placeholder localhost -- original: url_for('auth.login', _external=True),
        'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select',
        'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select',
    }
    auth_url = STEAM_OPENID_URL + '?' + '&'.join(f'{k}={v}' for k, v in params.items())     
    return redirect(auth_url)

@auth.route('/authorized')
def authorized():
    params = request.args.to_dict()
    params['openid.mode'] = 'check_authentication'
    response = requests.post(STEAM_OPENID_URL, data=params)

    if 'is_valid:true' not in response.text:
        return 'Authentication failed', 401
    
    steam_id = re.search(r'\/id\/(\d+)$', params.get('openid.claimed_id', ''))
    if not steam_id:
        return 'Could not extract Steam ID', 401
    steam_id = steam_id.group(1)

    user = User.query.filter_by(steam_id=steam_id).first()
    if not user:
        user = User(steam_id=steam_id, steam_username=steam_id) # TODO: Replace steam_username placeholder with real username from Steam Web API
        db.session.add(user)
        db.session.commit()

        login_user(user)
        return f'Logged in as Steam ID: {steam_id}'
    
    @auth.route('/Logout')
    @login_required
    def logout():
        logout_user()
        return 'Logged out'
