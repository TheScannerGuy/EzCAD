import os
from dotenv import load_dotenv

from flask import Flask

# Extensions
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_socketio import SocketIO
from flask_discord import DiscordOAuth2Session

db = SQLAlchemy()
ma = Marshmallow()
socketio = SocketIO()
discord = DiscordOAuth2Session()

load_dotenv()

ALLOWED_EXTENSIONS = {'json', 'mp3'}
UPLOAD_FOLDER = "app/uploads"


def create_app(debug=False):
    from app.main.api import api_blueprint
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"  # !! Only in development environment.

    # Flask-Discord Config
    app.config["DISCORD_CLIENT_ID"] = 926711959624233011  # Discord client ID.
    app.config["DISCORD_CLIENT_SECRET"] = os.getenv("DISCORD_CLIENT_SECRET")
    app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:5000/callback"  # URL to your callback endpoint.

    ma.init_app(app)
    db.init_app(app)
    socketio.init_app(app)
    discord.init_app(app)

    app.register_blueprint(api_blueprint, url_prefix='/api')

    with app.app_context():
        db.create_all()

    @app.before_first_request
    def create_tables():
        """ Pre-populate specific tables """
        from app.main.defaults import init_defaults
        init_defaults()

    return app


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
