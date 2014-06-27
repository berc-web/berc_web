from flask.ext.user import UserMixin
from hashlib import md5

from datetime import datetime

from flask.ext.security import UserMixin, RoleMixin
from sqlalchemy import event
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.orderinglist import ordering_list

from application import db


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
	password = db.Column(db.String(100))
	email = db.Column(db.String(100), unique=True)
	avatar = db.Column(db.String(200), unique=True, default=None)
	active = db.Column(db.Boolean(), nullable=False, default=False)
	confirmed_at = db.Column(db.DateTime())
	# Relationships
	roles = db.relationship('Role', secondary=user_roles,
					backref=db.backref('users', lazy='dynamic'))

	def __init__(self, first_name=None, last_name=None, username=None, password=None, email=None, avatar=None):
		self.first_name = first_name
		self.last_name 	= last_name
		self.username 	= username
		self.password 	= password
		self.email 		= email
		self.avatar 	= avatar

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


class TimestampMixin(object):
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow)

    def readable_date(self, date, format='%H:%M on %-d %B'):
        """Format the given date using the given format."""
        return date.strftime(format)