import os, re
from models import db, subscribed_user
from flask import Flask, request, session, g, redirect, url_for, abort, \
	render_template, flash
from flask.ext.admin import Admin, BaseView, expose
from admin_view import MyView

app = Flask(__name__)

# create corresponding admin system
admin = Admin(app, name='eecc2015')
admin.add_view(MyView(name='subscribers'))

# register the database with current app
db.app = app
db.init_app(app)

app.config.update(dict(
	DEBUG=True,
	SECRET_KEY='development',
	USERNAME='admin',
	PASSWORD='default'
))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
# app.config['SQLALCHEMY_DATABASE_URI'] = os.path.join()
app.config.from_envvar('BERC_SETTINGS', silent=True)

@app.route('/')
def home():
	return render_template('home.html')

def check_email(email):
	return re.match(r'[^@]+@[^@]+\.[^@]+', email)

@app.route('/subscribe', methods=['POST'])
def subscribe_email():
	if check_email(request.form['email']):
		user = subscribed_user(request.form['name'], request.form['email'])
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

if __name__ == '__main__':
	app.run()

