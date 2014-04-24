from flask import url_for, redirect, render_template, request
from models import LoginForm, RegistrationForm, User, db
from flask.ext import admin, login
from flask.ext.admin.contrib import sqla
from flask.ext.admin import helpers, expose, BaseView

# Create customized model view class
class MyModelView(sqla.ModelView):
	column_exclude_list = 'password'
	can_create = False

	def is_accessible(self):
		if login.current_user.is_authenticated():
			return login.current_user.is_admin()
		else:
			return False

class MyAdminIndexView(admin.AdminIndexView):

	@expose('/')
	def index(self):
		if not login.current_user.is_authenticated():
			return redirect(url_for('.login_view'))
		elif not login.current_user.is_admin():
			return redirect(url_for('.login_view'))
		return super(MyAdminIndexView, self).index()

	@expose('/login/', methods=['GET', 'POST'])
	def login_view(self):
		# handle user login
		form = LoginForm(request.form)
		if helpers.validate_form_on_submit(form):
			user = form.get_user()
			login.login_user(user)

		if login.current_user.is_authenticated() and login.current_user.is_admin():
			return redirect(url_for('.index'))

		self._template_args['form'] = form
		return super(MyAdminIndexView, self).index()

	@expose('/logout/')
	def logout_view(self):
		login.logout_user()
		return redirect(url_for('.index'))


class mailSenderView(BaseView):
	def is_accessible(self):
		if login.current_user.is_authenticated():
			return login.current_user.is_admin()
		else:
			return False

	@expose('/')
	def index(self):
		return self.render('admin/send_mail.html')
