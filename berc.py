import os, re
from models import db, subscribed_user, User
from admin_view import MyModelView, MyAdminIndexView
from flask import Flask, request, session, g, redirect, url_for, abort, \
	render_template, flash
from flask.ext import admin, login
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView

app = Flask(__name__)

app.config.update(dict(
	DEBUG=True,
	SECRET_KEY='eecc2015web',
	USERNAME='admin',
	PASSWORD='Berc12345',
	# SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://@localhost/testdb',
	SQLALCHEMY_DATABASE_URI=os.environ['DATABASE_URL'],
	SQLALCHEMY_ECHO=True
))

app.config.from_envvar('BERC_SETTINGS', silent=True)

# Initialize flask-login
def init_login():
	login_manager = login.LoginManager()
	login_manager.init_app(app)

	# create Admin user
	if db.session.query(User).filter_by(login=app.config['USERNAME']).count() == 0:
		admin = User()
		admin.login = app.config['USERNAME']
		admin.password = app.config['PASSWORD']
		db.session.add(admin)
		db.session.commit()

	# Create user Loader function
	@login_manager.user_loader
	def load_user(user_id):
		return db.session.query(User).get(user_id)

@app.route('/')
def home():
	return render_template('home.html')

def check_email(email):
	return re.match(r'[^@]+@[^@]+\.[^@]+', email)

@app.route('/subscribe', methods=['POST'])
def subscribe_email():
	if (request.form['name'] is None) or (request.form['name'] == ''):
		flash('Name can not be empty')
	elif check_email(request.form['email']):
		user = subscribed_user(request.form['name'], request.form['email'])
		db.session.add(user)
		try:
			db.session.commit()
		except Exception:
			flash('Email address already signed up.')
			return redirect(url_for('home')+'/#subscribe')
		flash('Thank you for your subscription!')
	else:
		flash('Invalid email address')
	return redirect(url_for('home')+'/#subscribe')

# register the database with current app
db.app = app
db.init_app(app)
init_login()

# create corresponding admin system
admin = admin.Admin(app, 'eecc', index_view=MyAdminIndexView(), base_template='my_master.html')
admin.add_view(MyModelView(User, db.session))
admin.add_view(ModelView(subscribed_user, db.session))

if __name__ == '__main__':
	app.run()
