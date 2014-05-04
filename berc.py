from flask import Flask, request, session, g, redirect, url_for, render_template
from flask.ext.babel import Babel
from flask.ext.mail import Mail
from flask.ext.admin import Admin
from admin_view import MyModelView, MyAdminIndexView
from config_user import user_manager
from models import db, User, Role

app = Flask(__name__)
	
app.config.from_object('config_berc.Config')

@app.route('/')
def home():
	return render_template('home.html')

db.app = app
db.init_app(app)
babel = Babel(app)
user_manager.init_app(app)
mail = Mail(app)
admin = Admin(app, 'eecc', index_view=MyAdminIndexView(), base_template='my_master.html')
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Role, db.session))

# try:
# 	if db.session.query(User).filter_by(username=app.config['USERNAME']).count() == 0:
# 		admin = User()
# 		admin.username = app.config['USERNAME']
# 		admin.password = user_manager.hash_password(app.config['PASSWORD'])
# 		admin.roles.append(Role(name='admin'))
# 		admin.active = True
# 		db.session.add(admin)
# 		db.session.commit()
# except Exception:
# 	pass
	
if __name__ == '__main__':
	app.run()
