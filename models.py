from flask.ext.sqlalchemy import SQLAlchemy
from wtforms import form, fields, validators
from passlib.hash import sha256_crypt
import re

db = SQLAlchemy()

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(30))
	last_name = db.Column(db.String(30))
	login = db.Column(db.String(50), unique=True)
	email = db.Column(db.String(100), unique=True)
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
	first_name =fields.TextField('First Name',[validators.required(),
											   validators.Length(max=30),])
	last_name = fields.TextField('Last Name', [validators.required(),
											   validators.Length(max=30)])
	email = 	fields.TextField('Email', 	  [validators.required(),
									   		   validators.Length(max=100)])
	login = 	fields.TextField('Username',  [validators.required(),
										  	   validators.Length(min=5, max=50)])

	password = 			fields.PasswordField('New Password', [
							validators.required(),
							validators.Length(min=6, max=20)])
	confirm_password = fields.PasswordField('Confirm Password', [
							validators.required(),
							validators.EqualTo('password', message='Passwords must match')])

	subscribe_confirm = fields.BooleanField('Subscribe our newsletter', default='True')

	def check_email(self, email):
		return re.match(r'[^@]+@[^@]+\.[^@]+', email)

	def validate_login(self, field):
		if db.session.query(User).filter_by(login=self.login.data).count() > 0:
			raise validators.ValidationError('Duplicate Username')


	def validate_email(self, field):
		if db.session.query(User).filter_by(email=self.email.data).count() > 0:
			raise validators.ValidationError('Email already signed up')
		if not self.check_email(self.email.data):
			raise validators.ValidationError('Invalid Email Address')

