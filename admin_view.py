from flask import url_for, redirect, render_template, request, flash
from models import User, db
from flask.ext import admin, login
from flask.ext.admin.contrib import sqla
from flask.ext.admin import expose
from flask.ext.user import roles_required

# import mailchimp

# apikey = '9ff33749afa74071578e2d427ec3a8b2-us8'

# Create customized model view class
class MyModelView(sqla.ModelView):
	column_exclude_list = 'password'
	# can_create = False

	def is_accessible(self):
		return login.current_user.is_authenticated()

class MyAdminIndexView(admin.AdminIndexView):

	@expose('/')
	# @roles_required('admin')
	def index(self):
		return super(MyAdminIndexView, self).index()

	@expose('/logout/')
	def logout_view(self):
		login.logout_user()
		return redirect(url_for('.index'))
