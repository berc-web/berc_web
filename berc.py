import os, re
from models import db, subscribed_user
from flask import Flask, request, session, g, redirect, url_for, abort, \
	render_template, flash
from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.contrib.sqla import ModelView

app = Flask(__name__)

# create corresponding admin system
admin = Admin(app, name='eecc2015')
admin.add_view(ModelView(subscribed_user, db.session))

# register the database with current app
db.app = app
db.init_app(app)

app.config.update(dict(
	DEBUG=True,
	SECRET_KEY='development',
	USERNAME='admin',
	PASSWORD='default'
))
# db_address='postgresql+psycopg2://jianzhongchen:CJZcps1230117@localhost/berc_dev'
db_address=os.environ['DATABASE_URL']
app.config['SQLALCHEMY_DATABASE_URI'] = db_address
# app.config['SQLALCHEMY_DATABASE_URI'] = os.path.join()
app.config.from_envvar('BERC_SETTINGS', silent=True)

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
			return redirect(url_for('home'))
		flash('Thank you for your subscription!')
	else:
		flash('Invalid emadcfzdsglkgjd;fslnimanimacaocaocaokjgil address')
	return redirect(url_for('home'))

if __name__ == '__main__':
	app.run()

