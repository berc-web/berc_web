from flask import url_for, redirect, render_template, request
from models import LoginForm, RegistrationForm, User, db
from flask.ext import admin, login
from flask.ext.admin.contrib import sqla
from flask.ext.admin import helpers, expose

# Create customized model view class
class MyModelView(sqla.ModelView):

	def is_accessible(self):
		return login.current_user.is_admin()

class MyAdminIndexView(admin.AdminIndexView):

	@expose('/')
	def index(self):
		if not login.current_user.is_authenticated():
			return redirect(url_for('.login_view'))
		return super(MyAdminIndexView, self).index()

	@expose('/login/', methods=['GET', 'POST'])
	def login_view(self):
		# handle user login
		form = LoginForm(request.form)
		if helpers.validate_form_on_submit(form):
			user = form.get_user()
			login.login_user(user)

		if login.current_user.is_authenticated():
			return redirect(url_for('.index'))
		link = '<p>Don\'t have an account? <a href="' + url_for('.register_view') + '">Click here to register.</a></p>'
		self._template_args['form'] = form
		self._template_args['link'] = link
		return super(MyAdminIndexView, self).index()

	@expose('/register/', methods=('GET', 'POST'))
	def register_view(self):
		form = RegistrationForm(request.form)
		if helpers.validate_form_on_submit(form):
			user = User()

			form.populate_obj(user)

			db.session.add(user)
			db.session.commit()

			login.login_user(user)
			return redirect(url_for('.index'))
		link = '<p>Already have an account? <a href="' + url_for('.login_view') + '">Click here to log in.</a></p>'
		self._template_args['form'] = form
		self._template_args['link'] = link
		return super(MyAdminIndexView, self).index()

	@expose('/logout/')
	def logout_view(self):
		login.logout_user()
		return redirect(url_for('.index'))
