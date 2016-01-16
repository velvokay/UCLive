from flask import Flask, render_template, redirect, url_for, json, request, session, flash, send_file
from werkzeug import generate_password_hash, check_password_hash
from functools import wraps
#import sqlite3

from app import application, db
from .models import BlogPost
from .reporttable import table
from enum import Enum
import csv, os.path

# login required decorator
def login_required(f):
		@wraps(f)
		def wrap(*args, **kwargs):
			if 'logged_in' in session:
				return f(*args, **kwargs)
			else:
				flash('Please login first.')
				return redirect(url_for('login'))
		return wrap
			

@application.route("/", methods=['GET', 'POST'])
def main():
	posts = db.session.query(BlogPost).all()
	main.major= None
	if request.method == 'POST':
		main.major = request.form['major']
		flash(str(main.major)+' was selected')
		return redirect(url_for('report'))
	return render_template('index.html', posts=posts)

@application.route('/dashBoard')
@login_required
def dashBoard():
	return render_template('dashboard.html')

@application.route("/displaySignUp")
def displaySignUp():
	return render_template("signup.html")

@application.route('/signUp',methods=['POST'])
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
	
@application.route('/login', methods=['GET', 'POST'])
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

@application.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('Successfully logged out.')
	return redirect(url_for('main'))
	
@application.route('/report')
def report():
	#main report page
	
	cols = {'campuses':['UCB', 'UCSD', 'UCLA', 'UCSB', 'UCI', 'UCD', 'UCSC', 'UCR', 'UCM']}
	rows = {'courses':['Calculus 1', 'Calculus 2', 'Calculus 3', 'Differential Equations', 'Linear Algebra', 'Discrete Math', 'Classical Mech.', 'Waves, Optics, Thermo.', 'Elec. & Mag.', 'Modern Physics', 'Intro to CS', 'Data Structs/Alg.', 'Intro Java'],
			'UCB':['Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes'],
			'UCSD':['Yes', 'Yes', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes'],
			'UCLA':['Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes'],
			'UCSB':['Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes'],
			'UCI':['Yes', 'Yes', 'No', 'No', 'No', 'No', 'No', 'No', 'No', 'No', 'Choose CS', 'Choose CS', 'Choose CS'],
			'UCD':['Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes'],
			'UCSC':['Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes'],
			'UCR':['Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes'],
			'UCM':['Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes']}
			
	_major = main.major
	
	#download as csv button
	
	subdirectory = "app/static/serve"
	try:
		os.mkdir(subdirectory)
	except Exception:
		pass
	
	class Campuses(Enum):
		UCB = 0
		UCSD = 1
		UCLA = 2
		UCSB = 3
		UCI = 4
		UCD = 5
		UCSC = 6
		UCR = 7
		UCM = 8
	
	with open(os.path.join(subdirectory, "ucRequirements.csv"), 'w') as csvfile:

		cols['campuses'].insert(0, 'Courses:')
		fieldnames = cols['campuses']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		
		writer.writeheader()
		count = 0
		for courses in range (0, len(rows['courses'])):
			writer.writerow({'Courses:': rows['courses'][count], 
			str(Campuses(0).name): rows[str(Campuses(0).name)][count], 
			str(Campuses(1).name): rows[str(Campuses(1).name)][count],
			str(Campuses(2).name): rows[str(Campuses(2).name)][count],
			str(Campuses(3).name): rows[str(Campuses(3).name)][count],
			str(Campuses(4).name): rows[str(Campuses(4).name)][count],
			str(Campuses(5).name): rows[str(Campuses(5).name)][count],
			str(Campuses(6).name): rows[str(Campuses(6).name)][count],
			str(Campuses(7).name): rows[str(Campuses(7).name)][count],
			str(Campuses(8).name): rows[str(Campuses(8).name)][count]
			})
			count = count + 1
			
	return render_template('report.html', _major=_major, table=table, cols=cols, rows=rows)
	
@application.route('/getCsv')
def getCsv():
	subdirectory = "static/serve"
	try:
		os.mkdir(subdirectory)
	except Exception:
		pass

	return send_file(os.path.join(subdirectory, "ucRequirements.csv"),
                     mimetype='text/csv',
                     attachment_filename='ucRequirements.csv',
                     as_attachment=True)


#def connect_db():
#	return sqlite3.connect(app.database)