from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.user import UserMixin, SQLAlchemyAdapter

db = SQLAlchemy()

user_roles = db.Table('user_roles',
	db.Column('id', db.Integer(), primary_key=True),
	db.Column('user_id', db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE')),
	db.Column('role_id', db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE')))

class Role(db.Model):
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(), unique=False)

	def __unicode__(self):
		return self.name

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(30))
	last_name = db.Column(db.String(30))
	username = db.Column(db.String(50), unique=True)
	email = db.Column(db.String(100), unique=True)
	password = db.Column(db.String(100))
	active = db.Column(db.Boolean(), nullable=False, default=False)
	confirmed_at = db.Column(db.DateTime())
	# Relationships
	roles = db.relationship('Role', secondary=user_roles,
					backref=db.backref('users', lazy='dynamic'))

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

db_adapter = SQLAlchemyAdapter(db, User)
