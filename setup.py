from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = '4e4fe810121af6b87c567c572bf2d868'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/imgurclone.db'
app.config['UPLOADS_FOLDER'] = os.path.join(os.getcwd(),"uploads")

db = SQLAlchemy(app)