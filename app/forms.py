from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Required
from .__init__ import db


class LoginForm(Form):
	openid = StringField('openid', validators=[DataRequired()])
	remember_me = BooleanField('remember_me', default=False)

class NameForm(Form):
	name = StringField('What is your name?', validators=[Required()])
	submit = SubmitField('Submit')
	
class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	
	def __repr__(self):
		return '<Role %r>' % self.name
	users = db.relationship('User', backref='role')
	
class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)
	
	def __repr__(self):
		return '<User %r>' % self.username
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))