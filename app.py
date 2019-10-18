import os

from flask import Flask
from flask_session import Session
from flask_socketio import SocketIO

app = Flask(__name__)

app.config.from_object("config.Configuration")
app.secret_key = os.getenv("SECRET_KEY")
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

socketio = SocketIO(app, manage_session=False)
