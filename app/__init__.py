from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_s3 import FlaskS3

#app object
app = Flask(__name__)

app.config['FLASKS3_BUCKET_NAME'] = 'ayakov.com'
s3 = FlaskS3(app)

app.secret_key = "alpine"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'

#create sqlalchemy object
db = SQLAlchemy(app)

from app import views, models

