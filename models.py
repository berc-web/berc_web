from berc import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.string(80))
	emain = db.Column(db.string(120), unique=True)

	def __init__(self, name, email):
		self.name = name
		self.email = email

	def __repr__(self):
		return '<Name: %r email: %r>' % self.name, self.email