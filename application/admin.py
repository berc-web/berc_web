from flask import url_for, redirect, render_template, request, flash
from models import User, Role, Team
from application import db, app
from flask.ext import admin, login
from flask.ext.admin.contrib import sqla
from flask.ext.admin import expose, Admin
from flask.ext.user import roles_required, login_required

# Create customized model view class
# ----------------------------------
class MyModelView(sqla.ModelView):
	column_exclude_list = 'password'
	# can_create = False

	def is_accessible(self):
		return login.current_user.is_authenticated()

class MyAdminIndexView(admin.AdminIndexView):

	@expose('/')
	@login_required
	@roles_required('admin')
	def index(self):
		return super(MyAdminIndexView, self).index()

	@expose('/logout/')
	@login_required
	def logout_view(self):
		login.logout_user()
		return redirect(url_for('.index'))

# Admin Setup
# -----------
admin = Admin(name='EECC Admin Panel', index_view=MyAdminIndexView(), base_template='my_master.html')
admin.add_view(MyModelView(User, db.session, category="models"))
admin.add_view(MyModelView(Role, db.session, category="models"))
admin.add_view(MyModelView(Team, db.session, category="models"))
admin.init_app(app)