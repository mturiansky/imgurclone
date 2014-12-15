from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, AnonymousUserMixin
import os

app = Flask(__name__)
app.secret_key = '4e4fe810121af6b87c567c572bf2d868'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/imgurclone.db'
app.config['UPLOADS_FOLDER'] = os.path.join(os.getcwd(),"uploads")

db = SQLAlchemy(app)

lm = LoginManager()
lm.login_view = "login"
lm.login_message = "Please log in to access this content."
lm.login_message_category = 'danger'
AnonymousUserMixin.name = u'Anonymous'
lm.anonymous_user = AnonymousUserMixin
lm.setup_app(app)