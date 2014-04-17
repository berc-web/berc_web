from flask.ext.sqlalchemy import SQLAlchemy
from wtforms import form, fields, validators
from passlib.hash import sha256_crypt

db = SQLAlchemy()

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(100))
	last_name = db.Column(db.String(100))
	login = db.Column(db.String(80), unique=True)
	email = db.Column(db.String(120), unique=True)
	password = db.Column(db.String(100))

	def is_authenticated(self):
		return True

	def is_admin(self):
		return self.login == 'admin'

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

		if not sha256_crypt.verify(self.password.data, user.password):
			raise validators.ValidationError('Invalid Password')

	def get_user(self):
		return db.session.query(User).filter_by(login=self.login.data).first()

class RegistrationForm(form.Form):
	first_name = fields.TextField(validators=[validators.required()])
	last_name = fields.TextField(validators=[validators.required()])
	email = fields.TextField(validators=[validators.required()])
	login = fields.TextField(validators=[validators.required()])
	password = fields.PasswordField(validators=[validators.required()])

	def validate_login(self, field):
		if db.session.query(User).filter_by(login=self.login.data).count() > 0:
			raise validators.ValidationError('Duplicate Username')

