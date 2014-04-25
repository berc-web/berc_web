import os

class Config(object):
	DEBUG=True
	SECRET_KEY='eecc2015web'
	USERNAME='admin'
	PASSWORD='Berc12345'

	if os.environ.get('DATABASE_URL') is None:
		SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://@localhost/localdb'
	else:
		SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

	SQLALCHEMY_ECHO=True

	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com'
	MAIL_PORT=465
	MAIL_USE_SSL=True
	MAIL_USERNAME = 'berc.web@gmail.com'
	MAIL_PASSWORD = 'Berc12345'
	# DEFAULT_MAIL_SENDER = 'EECC2015'

	# mandrill setup
	MANDRILL_API_KEY = 'n10PXMTcNEr7bvNKFWX7aw'