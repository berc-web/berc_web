import os
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, request, session, g, redirect, url_for, render_template, \
					flash, send_from_directory
from flask.ext.babel import Babel
from flask.ext.mail import Mail
from flask.ext.user import login_required, current_user, SQLAlchemyAdapter
from flask.ext.wtf.csrf import CsrfProtect
from werkzeug import secure_filename
from forms import AvatarForm
# config Scss
from flask.ext.scss import Scss

app = Flask(__name__)
app.config.from_object('config_berc.Config')

# Scss
Scss(app)

# Database
db = SQLAlchemy(app)
from models import User, Role

# db_adapter
db_adapter = SQLAlchemyAdapter(db, User)
from config_user import user_manager

# CsrfProtect
csrf = CsrfProtect(app)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/competition')
def competition():
	return render_template('competition.html')

@app.route('/news_and_resources')
def news_and_resources():
	return render_template('news.html')

@app.route('/about_us')
def about_us():
	return render_template('about.html')


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


@app.route('/upload_avatar', methods=['POST', 'GET'])
@login_required
@csrf.exempt
def upload_avatar():
	form = AvatarForm()
	if form.validate_on_submit():
		file_name = secure_filename(form.photo.data.filename)
		path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
		current_user.avatar = path
		db.session.commit()
		path = 'application' + path
		form.photo.data.save(path)
		return redirect(url_for('user'))

	return render_template('upload_avatar.html', form=form)

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
