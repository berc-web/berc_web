from flask.ext.user import UserMixin
from hashlib import md5

from datetime import datetime

from sqlalchemy import event
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.types import Enum

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
	fname = db.Column(db.String(30), nullable=False, default='')
	lname = db.Column(db.String(30), nullable=False, default='')
	username = db.Column(db.String(50), unique=True)
	password = db.Column(db.String(100))
	email = db.Column(db.String(100), unique=True)
	school = db.Column(db.String(100), nullable=False, default='')
	avatar = db.Column(db.String(200), unique=True, default=None)
	active = db.Column(db.Boolean(), nullable=False, default=False)
	subscribed = db.Column(db.Boolean(), default=False)
	confirmed_at = db.Column(db.DateTime())

	major = db.Column(db.String(50), default='')
	location = db.Column(db.String(2), default='')
	intro = db.Column(db.Text())

	# Relationships
	roles = db.relationship('Role', secondary=user_roles,
					backref=db.backref('users', lazy='dynamic'))
	team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=True)

	def is_active(self):
		return self.active

	def __unicode__(self):
		return self.username


class News(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), default="No Title")
	content = db.Column(db.Text())
	author = db.Column(db.String(100), default="No Author")
	time = db.Column(db.DateTime(), default=db.func.now())
	image = db.Column(db.String(200), unique=True, default=None)


class Team(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), unique=True, nullable=False)
	members = db.relationship('User', backref='team', lazy='dynamic')
	idea = db.relationship('Idea', backref='team', uselist=False)

	def __unicode__(self):
		return self.name


class Idea(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
	endorsement = db.Column(db.Integer)
	content = db.Column(db.Text())
