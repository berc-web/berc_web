import os, re
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, request, session, g, redirect, url_for, abort, \
	render_template, flash

app = Flask(__name__)

app.config.update(dict(
	DEBUG=True,
	SECRET_KEY='development',
	USERNAME='admin',
	PASSWORD='default'
))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config.from_envvar('BERC_SETTINGS', silent=True)
db = SQLAlchemy(app)

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
		db.session.commit()
		flash('Thank you for your subscription!')
	else:
		flash('Invalid email address')
	return redirect(url_for('home'))

@app.route('/emails', methods=['GET'])
def show_emails():
	entries = User.query.all()
	return render_template('show_emails.html', entries=entries)

#############
#	Models  #
#############
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	email = db.Column(db.String(120), unique=True)

	def __init__(self, name, email):
		self.name = name
		self.email = email

	def __repr__(self):
		return '<Name: %r email: %r>' % self.name, self.email
# ============================================================

if __name__ == '__main__':
	app.run()

