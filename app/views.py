from flask import Flask, render_template, redirect, url_for, json, request, session, flash
from werkzeug import generate_password_hash, check_password_hash
from functools import wraps
#import sqlite3

from app import app, db
from .models import BlogPost

# login requied decorator
def login_required(f):
		@wraps(f)
		def wrap(*args, **kwargs):
			if 'logged_in' in session:
				return f(*args, **kwargs)
			else:
				flash('Please login first.')
				return redirect(url_for('login'))
		return wrap
			

@app.route("/")
def main():
	posts = db.session.query(BlogPost).all()
	return render_template('index.html', posts=posts)

@app.route('/dashBoard')
@login_required
def dashBoard():
	return render_template('dashboard.html')

@app.route("/displaySignUp")
def displaySignUp():
	return render_template("signup.html")

@app.route('/signUp',methods=['POST'])
def signUp():
	#reads posted values from the form
	_name = request.form['inputName']
	_email = request.form['inputEmail']
	_password = request.form['inputPassword']
	
	#validates those values
	if _name and _email and _password:
	
		conn = mysql.connect()
		cursor = conn.cursor()
		hashed_password = generate_password_hash(_password)
		cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
		data = cursor.fetchall()
		
		if len(data) is 0:
			conn.commit()
			return json.dumps({'message':'User successfully posted to database! '})
		else:
			return json.dumps({'error':str(data[0])})
	else:
		return json.dumps({'html':'<span>Please enter the required fields.</span>'})
	
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			error = 'Invalid credentials. Please try again.'
		else:
			session['logged_in'] = True
			flash('Successfully logged in.')
			return redirect(url_for('main'))
	return render_template('login.html', error=error)
	
@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('Successfully logged out.')
	return redirect(url_for('main'))
	
#def connect_db():
#	return sqlite3.connect(app.database)

