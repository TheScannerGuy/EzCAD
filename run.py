import functools
import os.path
import sys

from app import create_app, discord
from flask import Flask, redirect, send_from_directory, render_template, url_for
from flask_discord import requires_authorization, Unauthorized
from os.path import exists
from app.main.api.unit import CurrentUnit

import app.main.schemas
from app.main.models import UserModel

from werkzeug.exceptions import NotFound

app = create_app(debug=True)  # Change to False in deployment

IGNORE_PATHS = ['login']
BUILD_PATH: str = "None"  # 'dist' folder needs full path


@app.route('/<path:path>', methods=['GET'])
@requires_authorization
def static_proxy(path):
    if exists(BUILD_PATH + r"/" + path):
        if path.endswith(".js"):
            return send_from_directory(BUILD_PATH, path, mimetype="application/javascript")
        return send_from_directory(BUILD_PATH, path)
    else:
        # If path doesn't exist fallback to index.html
        # https://angular.io/guide/deployment#routed-apps-must-fallback-to-indexhtml
        if not discord.authorized:
            return redirect(url_for('login'))
        if path.startswith('cad'):
            try:
                CurrentUnit().get()
            except NotFound:
                return redirect('/portal')

        return send_from_directory(BUILD_PATH, 'index.html')


@app.route('/')
@requires_authorization
def root():
    return send_from_directory(BUILD_PATH, 'index.html')


@app.route('/login')
def login():
    return discord.create_session(scope=['identify'])


@app.route('/callback')
def callback():
    """ Discord Auth Callback """
    discord.callback()
    user = discord.fetch_user()

    if UserModel.query.filter_by(discord_id=str(user.id)).first() is None:
        UserModel.register(user)

    return redirect('/portal')


@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect('/login')


if __name__ == "__main__":
    if sys.version_info[0] < 3 or sys.version_info[1] < 6:
        PY_VERSION = str(sys.version_info[0]) + "." + str(sys.version_info[1])
        print('ERROR: Invalid python version. Python 3.6 is required. Your are running: ', PY_VERSION)
    else:
        BUILD_PATH = os.path.abspath(os.getcwd()) + '/dist'
        app.run()
