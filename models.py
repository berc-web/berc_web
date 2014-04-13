from flask.ext.sqlalchemy import SQLAlchemy
from wtforms import form, fields, validators

db = SQLAlchemy()

class subscribed_user(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	email = db.Column(db.String(120), unique=True)

	def __init__(self, name, email):
		self.name = name
		self.email = email

	def __repr__(self):
		return '<Name: %r email: %r>' % self.name, self.email

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(100))
	last_name = db.Column(db.String(100))
	login = db.Column(db.String(80), unique=True)
	email = db.Column(db.String(120))
	password = db.Column(db.String(64))

	def __init__(self, login, email, password):
		self.login = login
		self.email = email
		self.password = password

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.id

	def __unicode__(self):
		return self.username

class LoginForm(form.Form):
	login = fields.TextField(validators=[validators.required()])
	password = fields.PasswordField(validators=[validators.required()])

	def validate_login(self, field):
		user = self.get_user()

		if user is None:
			raise validators.ValidationError('Invalid User')

		if user.password != self.password.data:
			raise validators.ValidationError('Invalid Password')

	def get_user(self):
		return db.session.query(User). filter_by(login=self.login.data).first()

class RegistrationForm(form.Form):
	login = fields.TextField(validators=[validators.required()])
	email = fields.TextField()
	password = fields.PasswordField(validators=[validators.required()])

	def validate_login(self, field):
		if db.session.query.filter_by(login=self.login.data).count() > 0:
			raise validators.ValidationError('Duplicate Username')

