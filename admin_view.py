from flask.ext.admin import Admin, BaseView, expose
from models import subscribed_user

class MyView(BaseView):
	@expose('/')
	def show_emails(self):
		entries = subscribed_user.query.all()
		return self.render('show_emails.html', entries=entries)