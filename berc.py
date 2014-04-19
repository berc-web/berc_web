import os, re
from models import db, User
from admin_view import MyModelView, MyAdminIndexView, RegistrationForm, \
	mailSenderView
from flask import Flask, request, session, g, redirect, url_for, abort, \
	render_template, flash
from flask.ext import admin, login
from flask.ext.admin import Admin
from flask.ext.mail import Mail, Message
from passlib.hash import sha256_crypt

app = Flask(__name__)

app.config.update(dict(
	DEBUG=True,
	SECRET_KEY='eecc2015web',
	USERNAME='admin',
	PASSWORD='Berc12345',
	# SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://@localhost/testdb',
	# SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://jianzhongchen:CJZcps1230117@localhost/berc_dev',
	SQLALCHEMY_DATABASE_URI=os.environ['DATABASE_URL'],
	SQLALCHEMY_ECHO=True,

	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'berc.web@gmail.com',
	MAIL_PASSWORD = 'Berc12345'
	# DEFAULT_MAIL_SENDER = 'EECC2015'
))

app.config.from_envvar('BERC_SETTINGS', silent=True)

# Initialize flask-login
def init_login():
	login_manager = login.LoginManager()
	login_manager.init_app(app)

	# create Admin user
	try:
		if db.session.query(User).filter_by(login=app.config['USERNAME']).count() == 0:
			admin = User()
			admin.login = app.config['USERNAME']
			admin.password = sha256_crypt.encrypt(app.config['PASSWORD'])
			db.session.add(admin)
			db.session.commit()
	except Exception:
		pass

	# Create user Loader function
	@login_manager.user_loader
	def load_user(user_id):
		return db.session.query(User).get(user_id)

@app.route('/')
def home():
	return render_template('home.html', form=RegistrationForm())


@app.route('/sign_up', methods=['POST'])
def sign_up():
	form = RegistrationForm(request.form)
	if not form.validate():
		flash("Invalid Registration Information.")
		return render_template('home.html', form=form)

	form = RegistrationForm(request.form)
	user = User()
	form.populate_obj(user)
	user.password = sha256_crypt.encrypt(user.password)
	db.session.add(user)
	db.session.commit()
	flash('Signed Up Successfully!')

	return redirect(url_for('home')+'/#sign_up')


@app.route('/send_email', methods=['POST'])
def send():
	subject = request.form['subject']
	content = request.form['content']

	mail = Mail(app)
	users = db.session.query(User)
	for user in users:
		if user.login != 'admin':
			msg = Message(recipients=[user.email],
						  body=content,
						  subject=subject,
						  sender="eecc2015")

			mail.send(msg)
			
	flash('emails sent Successfully')
	return redirect(url_for('home')+'admin/mailsenderview')

# register the database with current app
db.app = app
db.init_app(app)
init_login()

# create corresponding admin system
admin = admin.Admin(app, 'eecc', index_view=MyAdminIndexView(), base_template='my_master.html')
admin.add_view(MyModelView(User, db.session))
admin.add_view(mailSenderView(name='send'))

if __name__ == '__main__':
	app.run()
