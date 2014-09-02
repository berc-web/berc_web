import os
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, request, session, g, redirect, render_template, \
					flash, send_from_directory
from flask.ext.babel import Babel
from flask.ext.mail import Mail
from flask.ext.user import login_required, current_user, SQLAlchemyAdapter, roles_required
from flask.ext.user.views import register
from werkzeug import secure_filename
from forms import UpdateProfileForm, UploadNewsForm, TeammateInvitationForm
from postmonkey import PostMonkey
import boto


pm = PostMonkey('9ff33749afa74071578e2d427ec3a8b2-us8', timeout=10)

app = Flask(__name__)
app.config.from_object('config_berc.Config')

from flask_s3 import FlaskS3
from flask_s3 import url_for
s3 = FlaskS3(app)

# Scss
# config Scss
from flask.ext.scss import Scss
Scss(app)


# Database
db = SQLAlchemy(app)
from models import User, Role, Team, News


# db_adapter
db_adapter = SQLAlchemyAdapter(db, User)
from config_user import user_manager


@app.route('/')
def home():
	return render_template('home.html')


@app.route('/competition')
def competition():
	return render_template('competition.html')


@app.route('/rules')
def rules():
	return render_template('rules.html')


@app.route('/news_and_resources')
def news_and_resources():
	news_lst = db.session.query(News).all()
	return render_template('news.html', news_lst = news_lst)


@app.route('/news/<news_id>')
def news(news_id):
	news = db.session.query(News).filter(News.id==news_id)[0]
	return render_template('news/news_template.html', news=news)

@app.route('/about_us')
def about_us():
	return render_template('about.html')

@app.route('/request_list')
def request_list():
	# TODO
	return render_template('request_list.html')

@app.route('/users')
def user_lst():
	return render_template('users.html')


@app.route('/profile', methods=['GET'])
@login_required
def user():
	invitation_list = db.session.query(User).filter_by(User.request_teammate==current_user.id).all()
	invitation_list = [user.username for user in invitation_list]
	return render_template('user_profile.html', user=current_user, inv_list=invitation_list)

@app.route('/invitation')
def invitation():
	# TODO
	return render_template('invitation.html', user=current_user)

@app.route('/<uname>/profile', methods=['GET'])
@login_required
def userProfile(uname):
	if uname == current_user.username:
		return redirect(url_for('user'))

	user = user_manager.find_user_by_username(uname)
	if user is None:
		flash('User '+uname+' not found.', 'error')
		return redirect(url_for('home'))
	else:
		return render_template('user_profile.html', user=user)


def upload_s3(file_name, data):
	connection = boto.connect_s3(app.config['AWS_ACCESS_KEY_ID'],
		app.config['AWS_SECRET_ACCESS_KEY'])
	bucket = connection.get_bucket(app.config['S3_BUCKET_NAME'])
	file_path = os.path.join(app.config['S3_UPLOAD_DIRECTORY'], file_name)
	sml = bucket.new_key(os.path.join('static', file_path))
	path = url_for('static', filename=file_path)
	sml.set_contents_from_file(data)
	sml.set_acl('public-read')
	return path


@app.route('/update_profile', methods=['POST', 'GET'])
@login_required
def update_profile():
	form = UpdateProfileForm()
	if form.validate_on_submit():

		# update avatar
		if form.photo.data:
			file_name = secure_filename(form.photo.data.filename)
			extension = file_name.split('.')[-1]
			file_name = '.'.join([current_user.username, extension])
			path = upload_s3(file_name, form.photo.data)
			current_user.avatar = path

		current_user.fname = form.fname.data
		current_user.lname = form.lname.data
		current_user.school = form.school.data
		current_user.major = form.major.data
		current_user.intro = form.intro.data
		current_user.location = form.location.data

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


@app.route('/news_upload', methods=['POST'])
@login_required
@roles_required('admin')
def admin_news_uploads():
	form = UploadNewsForm()
	if form.validate_on_submit():
		news = News()
		db.session.add(news)
		db.session.commit()
		news.title = form.title.data
		news.content = form.content.data
		news.author = current_user.username

		file_name = secure_filename(form.image.data.filename)
		extension = file_name.split('.')[-1]
		file_name = '.'.join([str(news.id), extension])
		path = upload_s3(file_name, form.image.data)
		news.image = path
		db.session.commit()
	return redirect(url_for('news_and_resources'))


@app.route('/team_invitation', methods=['POST'])
def team_invitation():
	form = TeammateInvitationForm()
	user = None
	if form.email.data:
		user = user_manager.find_user_by_email(form.email.data)
	elif form.username.data:
		user = user_manager.find_user_by_username(form.username.data)

	if not user:
		flash("User does not exist.", 'error')
		return redirect(url_for('invitation'))

	if current_user.team_id or user.team_id:
		flash("Not both members are available to form a new team.", 'error')
	elif current_user.request_teammate:
		flash("You can only send one request at the same time. You have to wait for a response before you send your next request.", 'error')
	else:
		send_mail(user, 'invitation', sender=current_user)
		current_user.request_teammate = user.id
		db.session.commit()
		flash("Invitation sent. You will be notified by email when he/she make a decision.", 'success')

	return redirect(url_for('invitation'))


@app.route('/invitation/accept/<uname>', methods=['POST'])
def accept_invitation(uname):
	user = user_manager.find_user_by_username(uname)
	if user.team_id:
		flash('This user has already formed a team with someone else. Please pick another teammate.', 'error')
		return redirect(url_for('request_list'))
	else:
		team = Team()
		team.members.append(current_user)
		team.members.append(user)
		db.session.add(team)
		user.request_teammate = None
		current_user.request_teammate = None

		lst1 = db.session.query(User).filter_by(User.request_teammate==user_id).all()
		lst2 = db.session.query(User).filter_by(User.request_teammate==current_user.id).all()
		user_lst = lst1.extend(lst2)

		for usr in user_lst:
			usr.request_teammate = None
			send_mail(usr, 'fail_invitation')

		# TODO
		send_mail(user, 'new_team', u1=user, u2=current_user)
		send_mail(current_user, 'new_team', u1=user, u2=current_user)


@app.route('/invitation/reject/<uname>', methods=['POST'])
def reject_invitation(uname):
	user = user_manager.find_user_by_username(uname)
	user.request_teammate = None
	send_mail(user, 'fail_invitation')


def send_mail(user, theme, **kwargs):
	subject = render_template('emails/'+theme+'_subject.txt',  user=user, **kwargs)
	subject = subject.replace('\n', ' ')
	subject = subject.replace('\r', ' ')
	html_message = render_template('emails/'+theme+'_message.html',  user=user, **kwargs)
	text_message = render_template('emails/'+theme+'_message.txt',  user=user, **kwargs)
	user_manager.send_email_function(user.email, subject, html_message, text_message)


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
	if db.session.query(User).filter_by(User.username==app.config['USERNAME']).count() == 0:
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
