import os
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, request, session, g, redirect, render_template, \
					flash, send_from_directory
from flask.ext.babel import Babel
from flask.ext.mail import Mail
from flask.ext.user import login_required, current_user, SQLAlchemyAdapter, roles_required
from flask.ext.user.views import register
from werkzeug import secure_filename
from forms import UpdateProfileForm, UploadNewsForm, TeammateInvitationForm, \
					UpdateTeamInfoForm, CommentForm, UploadCompArticleForm, \
					SendNotificationForm, CommentReplyForm, CommentEditForm
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
from models import User, Role, Team, News, Idea, Comment, Notification, \
					PersonalNotification


# db_adapter
db_adapter = SQLAlchemyAdapter(db, User)
from config_user import user_manager


@app.route('/')
def home():
	if app.config['LANGUAGE'] == 'en':
		return render_template('home.html')
	else:
		return render_template('home_ch.html')


@app.route('/competition')
def competition():
	if app.config['LANGUAGE'] == 'en':
		return render_template('competition.html')
	else:
		return render_template('competition_ch.html')


@app.route('/event')
def event():
	return render_template('event.html')


@app.route('/rules')
def rules():
	if app.config['LANGUAGE'] == 'en':
		return render_template('rules.html')
	else:
		return render_template('rules_ch.html')


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
@login_required
def request_list():
	return render_template('request_list.html')


@app.route('/users')
@login_required
def all_users():
	users = db.session.query(User).all()
	return render_template('users.html', users = users)


@app.route('/profile', methods=['GET'])
@login_required
def user():
	invitation_list = db.session.query(User).filter(User.request_teammate==current_user.id).all()
	invitation_list = [user.username for user in invitation_list]
	return render_template('user_profile.html', user=current_user, inv_list=invitation_list)


@app.route('/invitation')
@login_required
def invitation():
	return render_template('invitation.html', user=current_user)


@app.route('/teams')
@login_required
def all_teams():
	teams = db.session.query(Team).all()
	return render_template('teams.html', teams = teams)


@app.route('/disp_ideas')
@login_required
def all_ideas():
	#TODO
	ideas = db.session.query(Idea).all()
	# return render_template("xxxxx.html", ideas = ideas)


@app.route('/notifications')
@login_required
def personal_notifications():
	notifications = current_user.notification
	return render_template("personal_notifications.html", notifications=notifications)


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
		return render_template('user_view.html', user=user)


@app.route('/teams/<teamId>', methods=['GET'])
@login_required
def teamProfile(teamId):
	if int(teamId) == int(current_user.team_id):
		return redirect(url_for('team_page'))
	form = CommentForm()
	team = db.session.query(Team).filter(Team.id == teamId).first()
	comments = db.session.query(Comment).filter(Comment.idea_id == team.idea.id).all()
	if team is None:
		flash('Team '+teamId+' not found.', 'error')
		return redirect(url_for('home'))
	else:
		return render_template('team_view.html', form=form, team=team, comments=comments)


def upload_s3(file_name, data, directory):
	connection = boto.connect_s3(app.config['AWS_ACCESS_KEY_ID'],
		app.config['AWS_SECRET_ACCESS_KEY'])
	bucket = connection.get_bucket(app.config['S3_BUCKET_NAME'])
	file_path = os.path.join(directory, file_name)
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
			path = upload_s3(file_name, form.photo.data, app.config['S3_UPLOAD_DIRECTORY'])
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
			pass

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
		path = upload_s3(file_name, form.image.data, app.config['S3_NEWS_IMAGE_DIR'])
		news.image = path
		db.session.commit()
	return redirect(url_for('news_and_resources'))


@app.route('/team_invitation', methods=['POST'])
@login_required
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
	elif current_user.location != user.location:
		flash("You can only form team with people from the same location(US or CH)", "error")
	else:
		send_mail(user, 'invitation', sender=current_user)
		current_user.request_teammate = user.id
		db.session.commit()
		flash("Invitation sent. You will be notified by email when he/she makes a decision.", 'success')

	return redirect(url_for('invitation'))


@app.route('/invitation/accept/<uname>', methods=['POST'])
@login_required
def accept_invitation(uname):
	user = user_manager.find_user_by_username(uname)
	if user.team_id:
		flash('This user has already formed a team with someone else. Please pick another teammate.', 'error')
		return redirect(url_for('user'))
	else:
		team = Team()
		team.members.append(current_user)
		team.members.append(user)
		team.name = current_user.username

		db.session.add(team)
		user.request_teammate = None
		current_user.request_teammate = None

		lst1 = db.session.query(User).filter(User.request_teammate==user.id).all()
		lst2 = db.session.query(User).filter(User.request_teammate==current_user.id).all()
		lst1.extend(lst2)

		for usr in lst1:
			usr.request_teammate = None
			send_mail(usr, 'fail_invitation')

		send_mail(user, 'new_team', u1=user, u2=current_user)
		send_mail(current_user, 'new_team', u1=user, u2=current_user)
		db.session.commit()

		team.name = "New Team No." + str(team.id)
		team.idea = Idea()
		db.session.commit()

		return redirect(url_for('team_page'))


@app.route('/invitation/reject/<uname>', methods=['POST'])
@login_required
def reject_invitation(uname):
	user = user_manager.find_user_by_username(uname)
	user.request_teammate = None
	send_mail(user, 'fail_invitation')

	return redirect(url_for('user'))


@app.route('/team', methods=['GET', 'POST'])
@login_required
def team_page():
	team_id = current_user.team_id
	team = db.session.query(Team).filter(Team.id == team_id).first()

	if team:
		comments = db.session.query(Comment).filter(Comment.idea_id == team.idea.id).all()
		notifs = db.session.query(Notification).order_by(Notification.time).limit(10).all()

		return render_template("team_profile.html", team = team, \
			show_result = app.config['COMPETATION_CLOSED'], notifications = notifs, comments=comments)
	else:
		flash("You have not formed a team yet.")
		return redirect(url_for("invitation"))


@app.route('/update_team', methods=['POST', 'GET'])
@login_required
def update_team():
	form = UpdateTeamInfoForm()
	team_id = current_user.team_id
	team = db.session.query(Team).filter(Team.id == team_id).first()
	if form.validate_on_submit():
		if team:
			team.name = form.name.data
			team.idea.content = form.idea.data
			team.caseNumber = int(form.caseNumber.data)
			db.session.commit()
			return redirect(url_for('team_page'))
		else:
			flash("Team does not exist.", "error")
			return redirect(url_for('invitation'))

	return render_template('team_update.html', form=form, team=team)


@app.route('/team_upload', methods=['POST', 'GET'])
@login_required
def team_upload():
	team_id = current_user.team_id
	team = db.session.query(Team).filter(Team.id == team_id).first()
	if team:
		form = UploadCompArticleForm()
		if form.validate_on_submit():
			file_name = "team"+str(team.id)+".pdf"
			team.submission = upload_s3(file_name, form.article.data, app.config['S3_COMP_DIR'])
			db.session.commit()
		return render_template("team_upload.html", form=form, team=team)
	else:
		flash("You have not formed a team yet.")
		return redirect(url_for("invitation"))


@app.route('/team_notifications')
@login_required
def team_notifications():
	team_id = current_user.team_id
	team = db.session.query(Team).filter(Team.id == team_id).first()
	notifications = db.session.query(Notification).order_by(Notification.time).all()
	return render_template("team_notifications.html", notifications=notifications, team=team)


@app.route('/dismiss_team', methods=['POST'])
@login_required
def dismiss_team():
	team_id = current_user.team_id
	team = db.session.query(Team).filter(Team.id == team_id).first()
	for cmt in team.idea.comment:
		db.session.delete(cmt)
	db.session.delete(team.idea)
	db.session.delete(team)
	db.session.commit()
	flash("Team dismissed.", "success")
	return redirect(url_for('invitation'))


@app.route('/comment_idea/<idea_id>', methods=['POST', 'GET'])
@login_required
def comment_idea(idea_id):
	form = CommentForm()
	idea = db.session.query(Idea).filter(Idea.id == idea_id).first()
	team = db.session.query(Team).filter(Team.id == idea.team_id).first()
	if form.validate_on_submit():
		if idea:
			comment = Comment()
			comment.content = form.comment.data
			idea.comment.append(comment)
			current_user.comment.append(comment)
			db.session.add(comment)

			for member in comment.idea.team.members:
				notif = PersonalNotification()
				notif.content = current_user.username + " commented on your team's idea."
				member.notification.append(notif)

			db.session.commit()
			return redirect(url_for('teamProfile', teamId=team.id))
		else:
			flash("Idea does not exist.", "error")
			return redirect(url_for('all_ideas'))

	return render_template('comment_idea.html', form=form, idea_id=idea_id, team=team)


@app.route('/comment/<comment_id>/edit', methods=['POST', 'GET'])
@login_required
def edit_comment(comment_id):
	form = CommentEditForm()
	comment = db.session.query(Comment).filter(Comment.id == comment_id).first()
	if not comment:
		flash("Invalid Comment", "error")
		return redirect(url_for("teamProfile", teamId=current_user.team.id))

	origin_comment = comment
	while (origin_comment.parent != None):
		origin_comment = origin_comment.parent
	team = origin_comment.idea.team

	if comment.user_id != current_user.id:
		flash("You are not authorized to edit other people's comments", "error")
		return redirect(url_for("teamProfile", teamId=team.id))

	if form.validate_on_submit():
		comment.content = form.modified.data
		db.session.commit()
		flash("Comment updated.", "success")
		return redirect(url_for('teamProfile', teamId=team.id))

	# TODO
	# return render_template('edit_comment.html', form=form, comment=comment)


@app.route('/comment/<comment_id>/reply', methods=['POST', 'GET'])
@login_required
def reply_comment(comment_id):
	form = CommentReplyForm()
	comment = db.session.query(Comment).filter(Comment.id == comment_id).first()
	if not comment:
		flash("Invalid comment.", "error")
		return redirect(url_for(''))

	origin_comment = comment
	while (origin_comment.parent != None):
		origin_comment = origin_comment.parent
	team = origin_comment.idea.team
	if form.validate_on_submit():
		comment.reply.append(Comment(content = form.reply.data, user=current_user))
		db.session.commit()
		notify(comment.user, current_user.username + " replied your comment.")
		return redirect(url_for('teamProfile', teamId=team.id))

	return render_template('reply_comment.html', form=form, comment=comment)


@app.route('/notification/<notif_id>/delete')
@login_required
def delete_notification(notif_id):
	notif = db.session(PersonalNotification).filter(PersonalNotification.id == notif_id)
	notif.user.notification.remove(notif)
	db.session.delete(notif)
	db.session.commit()
	return redirect(url_for('personal_notifications'))


@app.route('/send_notification', methods=['POST'])
@login_required
@roles_required('admin')
def send_notification():
	form = SendNotificationForm()
	if form.validate_on_submit():
		noti = Notification()
		noti.content = form.notification.data
		db.session.add(noti)
		db.session.commit()

	return redirect(url_for('notify.send_notification'))


def comment_view(comments):
	form = CommentReplyForm()
	return render_template('comment_view.html', comments=comments, form=form)
app.jinja_env.globals.update(comment_view=comment_view)

def send_mail(user, theme, **kwargs):
	subject = render_template('emails/'+theme+'_subject.txt',  user=user, **kwargs)
	subject = subject.replace('\n', ' ')
	subject = subject.replace('\r', ' ')
	html_message = render_template('emails/'+theme+'_message.html',  user=user, **kwargs)
	text_message = render_template('emails/'+theme+'_message.txt',  user=user, **kwargs)
	user_manager.send_email_function(user.email, subject, html_message, text_message)


def notify(user, content):
	notif = PersonalNotification()
	notif.content = content
	db.session.add(notif)
	user.notification.append(notif)
	db.session.commit()


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
	if db.session.query(User).filter(User.username==app.config['USERNAME']).count() == 0:
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
