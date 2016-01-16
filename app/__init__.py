from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_s3 import FlaskS3
from config import basedir

#application object
application = Flask(__name__)
application.config.from_object('config')

application.config['FLASKS3_BUCKET_NAME'] = 'ayakov.com'
s3 = FlaskS3(application)

application.secret_key = "alpine"

application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db' #local db is here

#create sqlalchemy object
db = SQLAlchemy(application)

from app import views, models

