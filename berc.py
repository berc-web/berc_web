import os
from flask import Flask, request, session, g, redirect, url_for, render_template, \
					flash, send_from_directory
from flask.ext.babel import Babel
from flask.ext.mail import Mail
from flask.ext.admin import Admin
from flask.ext.user import login_required, current_user
from admin_view import MyModelView, MyAdminIndexView
from config_user import user_manager
from models import db, User, Role
from werkzeug import secure_filename

app = Flask(__name__)
app.config.from_object('config_berc.Config')
ALLOWED_PIC = set(['jpg', 'jpe', 'jpeg', 'png', 'gif', 'svg', 'bmp'])

def file_allowed(filename, ext_set):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ext_set

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/user/<uname>', methods=['GET'])
@login_required
def user(uname):
	user = user_manager.find_user_by_username(uname)
	if user is None:
		flash('User '+uname+' not found.')
		return redirect(url_for('home'))
	else:
		return render_template('user.html', user=user)

@app.route('/user/upload_avatar', methods=['POST', 'GET'])
@login_required
def upload_avatar():

	##### DELETE OLD AVATAR FILE WHEN USER UPLOAD A NEW ONE #####
	# path = os.path.join(app.config['UPLOAD_FOLDER'], 'user_avatar')
	# filename = current_user.avatar.split('/')[-1]
	# current = send_from_directory(path, filename)
	# if current:
	# 	current.delete()

	file  = request.files['avatar']
	filename = secure_filename(file.filename)
	if file and file_allowed(filename, ALLOWED_PIC):
		path = os.path.join(app.config['UPLOAD_FOLDER'], 'user_avatar', filename)
		file.save(path)
		current_user.avatar = os.path.join('..', path)
		db.session.commit()
	return redirect(url_for('user', uname=current_user.username))

db.init_app(app)
babel = Babel(app)
user_manager.init_app(app)
mail = Mail(app)
admin = Admin(app, 'eecc', index_view=MyAdminIndexView(), base_template='my_master.html')
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Role, db.session))

try:
	if db.session.query(User).filter_by(username=app.config['USERNAME']).count() == 0:
		admin = User()
		admin.username = app.config['USERNAME']
		admin.password = user_manager.hash_password(app.config['PASSWORD'])
		admin.roles.append(Role(name='admin'))
		admin.active = True
		db.session.add(admin)
		db.session.commit()
except Exception:
	pass
	
if __name__ == '__main__':
	app.run()
