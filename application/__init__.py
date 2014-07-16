import os
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, request, session, g, redirect, url_for, render_template, \
					flash, send_from_directory
from flask.ext.babel import Babel
from flask.ext.mail import Mail
from flask.ext.user import login_required, current_user, SQLAlchemyAdapter
from flask.ext.user.views import register
from werkzeug import secure_filename
from forms import UpdateProfileForm
from postmonkey import PostMonkey

pm = PostMonkey('9ff33749afa74071578e2d427ec3a8b2-us8', timeout=10)


app = Flask(__name__)
app.config.from_object('config_berc.Config')


from flask_s3 import FlaskS3
s3 = FlaskS3(app)


# Database
db = SQLAlchemy(app)
from models import User, Role


# db_adapter
db_adapter = SQLAlchemyAdapter(db, User)
from config_user import user_manager


@app.route('/')
def home():
	return render_template('home.html')


@app.route('/profile', methods=['GET'])
@login_required
def user():
	return render_template('user_profile.html', user=current_user)


@app.route('/<uname>/profile', methods=['GET'])
@login_required
def userProfile(uname):
	if uname == current_user.username:
		return redirect(url_for('user'))

	user = user_manager.find_user_by_username(uname)
	if user is None:
		flash('User '+uname+' not found.')
		return redirect(url_for('home'))
	else:
		return render_template('user_profile.html', user=user)


@app.route('/update_profile', methods=['POST', 'GET'])
@login_required
def update_profile():
	form = UpdateProfileForm()
	if form.validate_on_submit():

		# update avatar
		if form.photo.data:
			file_name = secure_filename(form.photo.data.filename)
			filename = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
			path = url_for('static', filename = filename)
			current_user.avatar = path
			path = 'application' + path
			form.photo.data.save(path)

		current_user.fname = form.fname.data
		current_user.lname = form.lname.data
		current_user.school = form.school.data

		try:
			pm.listUnsubscribe(id='8d4e6caca8', email_address=current_user.email)
		except Exception, e:
			pass

		current_user.email = form.email.data

		db.session.commit()

		try:
			pm.listSubscribe(id='8d4e6caca8', email_address=current_user.email, double_optin=False)
		except Exception, e:
			passm

		return redirect(url_for('user'))

	return render_template('update_profile.html', form=form, user=current_user)


babel = Babel(app)
user_manager.init_app(app)

mail = Mail(app)


# Debug toolbar
# -------------
from flask_debugtoolbar import DebugToolbarExtension
toolbar = DebugToolbarExtension(app)


# Admin
# -----
import admin


# Init admin user
# ---------------
try:
	if db.session.query(User).filter_by(username=app.config['USERNAME']).count() == 0:
		admin = User()
		admin.username = app.config['USERNAME']
		admin.email = app.config['ADMIN_EMAIL']
		admin.password = user_manager.hash_password(app.config['PASSWORD'])
		admin.roles.append(Role(name='admin'))
		admin.active = True
		db.session.add(admin)
		db.session.commit()
except Exception:
	pass
