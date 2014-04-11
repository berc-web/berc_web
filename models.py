from flask.ext.sqlalchemy import SQLAlchemy

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
	name = db.Column(db.String(80))
	email = db.Column(db.String(120), unique=True)

	def __init__(self, name, email):
		self.name = name
		self.email = email

	def __repr__(self):
		return '<Name: %r email: %r>' % self.name, self.email