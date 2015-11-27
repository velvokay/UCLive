from flask import render_template, flash, redirect, session, url_for, Flask
from app import app
from .forms import LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from . import auth

@app.route('/')
@app.route('/index')
def index():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.openid.data).first()
		if user is None:
			user = User(username = form.openid.data)
			db.session.add(user)
			session['known'] = False
		else:
			session['known'] = True
		session['name'] = form.openid.data
		form.openid.data = ''
		return redirect(url_for('index'))
	
	posts = [ #fake array of posts
		{
			'author': {'nickname': 'John'},
			'body': 'Hi, my name is John!'
		},
		{
			'author': {'nickname': 'David'},
			'body': 'This is David.'
		}
	]
	
	return render_template("index.html",
							title='Home',
							form = form,
							name= session.get('name'),
							known = session.get('known', False),
							posts=posts)
							
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)
							
