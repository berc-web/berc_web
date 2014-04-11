import os, re
from models import db, User
from flask import Flask, request, session, g, redirect, url_for, abort, \
	render_template, flash
from flask.ext.admin import Admin

app = Flask(__name__)
admin = Admin(app)
db.init_app(app)

app.config.update(dict(
	DEBUG=True,
	SECRET_KEY='development',
	USERNAME='admin',
	PASSWORD='default'
))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config.from_envvar('BERC_SETTINGS', silent=True)

# @app.teardown_appcontext

@app.route('/')
def home():
	return render_template('home.html')

def check_email(email):
	return re.match(r'[^@]+@[^@]+\.[^@]+', email)

@app.route('/subscribe', methods=['POST'])
def subscribe_email():
	if check_email(request.form['email']):
		user = User(request.form['name'], request.form['email'])
		db.session.add(user)
		try:
			db.session.commit()
		except Exception:
			flash('Email address already signed up.')
			return redirect(url_for('home'))
		flash('Thank you for your subscription!')
	else:
		flash('Invalid email address')
	return redirect(url_for('home'))

@app.route('/emails', methods=['GET'])
def show_emails():
	entries = User.query.all()
	return render_template('show_emails.html', entries=entries)

if __name__ == '__main__':
	app.run()

