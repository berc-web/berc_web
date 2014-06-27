import os
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, request, session, g, redirect, url_for, render_template, \
					flash, send_from_directory
from flask.ext.babel import Babel
from flask.ext.mail import Mail
from flask.ext.user import login_required, current_user, SQLAlchemyAdapter
from werkzeug import secure_filename

app = Flask(__name__)
app.config.from_object('config_berc.Config')
ALLOWED_PIC = set(['jpg', 'jpe', 'jpeg', 'png', 'gif', 'svg', 'bmp'])

# Database
db = SQLAlchemy(app)
from models import User, Role

# db_adapter
db_adapter = SQLAlchemyAdapter(db, User)
from config_user import user_manager

def file_allowed(filename, ext_set):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ext_set

@app.route('/')
def home():
	return render_template('home.html')


@app.route('/user/<uname>', methods=['GET'])
@login_required
def user(uname):
	if uname != current_user.username:
		return redirect(url_for('userProfile', uname=current_user.username, uname2=uname))

	user = user_manager.find_user_by_username(uname)
	if user is None:
		flash('User '+uname+' not found.')
		return redirect(url_for('home'))
	else:
		return render_template('user.html', user=user)


@app.route('/user/<uname>/viewprofile/<uname2>', methods=['GET'])
@login_required
def userProfile(uname, uname2):
	if uname != current_user.username:
		return redirect(url_for('userProfile', uname=current_user.username, uname2=uname2))

	user = user_manager.find_user_by_username(uname2)
	if user is None:
		flash('User '+uname2+' not found.')
		return redirect(url_for('home'))
	else:
		return render_template('profile.html', user=user)


@app.route('/user/<uname>/upload_avatar', methods=['POST'])
@login_required
def upload_avatar(uname):
	if uname != current_user.username:
		flash("You are not autorized to modify the profile of user: " + uname)
		return redirect(url_for('home')+'/admin')

	##### DELETE OLD AVATAR FILE WHEN USER UPLOAD A NEW ONE #####
	# path = os.path.join(app.config['UPLOAD_FOLDER'], 'user_avatar')
	# filename = current_user.avatar.split('/')[-1]
	# current = send_from_directory(path, filename)
	# if current:
	# 	current.delete()

	file  = request.files['avatar']
	filename = secure_filename(file.filename)
	if file and file_allowed(filename, ALLOWED_PIC):
		path = url_for('static', filename=os.path.join('upload', 'user_avatar', filename))
		current_user.avatar = os.path.join('..', path)
		db.session.commit()
		path = 'application' + path
		file.save(path)
	return redirect(url_for('user', uname=current_user.username))

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

if __name__ == '__main__':
	app.run()
