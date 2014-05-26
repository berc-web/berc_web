import os
from flask import url_for

class Config(object):
	DEBUG=True
	SECRET_KEY='eecc2015web'
	USERNAME='admin'
	PASSWORD='Berc12345'

	if os.environ.get('DATABASE_URL') is None:
		# SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://@localhost/localdb'
		SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://@localhost/v2db'
		# SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://jianzhongchen:CJZcps1230117@localhost/berc_dev'
	else:
		SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

	SQLALCHEMY_ECHO=True

	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com'
	MAIL_PORT=465
	MAIL_USE_SSL=True
	MAIL_USERNAME = 'eecc2015@gmail.com'
	MAIL_PASSWORD = 'Berc12345'
	MAIL_DEFAULT_SENDER = 'eecc2015@gmail.com'

	# FLASK-USER URL CONFIG
	USER_CHANGE_PASSWORD_URL  = '/change-password'
	USER_CHANGE_USERNAME_URL  = '/change-username'
	USER_CONFIRM_EMAIL_URL    = '/confirm-email/<token>'
	USER_FORGOT_PASSWORD_URL  = '/forgot-password'
	USER_REGISTER_URL         = '/register'
	USER_RESET_PASSWORD_URL   = '/reset-password/<token>'
	USER_LOGIN_URL            = '/login'
	USER_LOGOUT_URL           = '/logout'

	# FLASK-USER TEMPLATES
	# USER_LOGIN_TEMPLATE                     = 'flask_user/login.html'
	# USER_REGISTER_TEMPLATE                  = 'flask_user/register.html'
	# USER_CHANGE_PASSWORD_TEMPLATE           = 'flask_user/change_password.html'
	# USER_CHANGE_USERNAME_TEMPLATE           = 'flask_user/change_username.html'
	# USER_FORGOT_PASSWORD_TEMPLATE           = 'flask_user/forgot_password.html'
	# USER_RESET_PASSWORD_TEMPLATE            = 'flask_user/reset_password.html'

	UPLOAD_FOLDER = 'static/upload'
	# DEFAULT_FILE_STORAGE = 'filesystem'
