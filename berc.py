import os, re
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, request, session, g, redirect, url_for, abort, \
	render_template, flash

app = Flask(__name__)

app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'berc.db'),
	DEBUG=True,
	SECRET_KEY='development',
	USERNAME='admin',
	PASSWORD='default'
))
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config.from_envvar('BERC_SETTINGS', silent=True)
db = SQLAlchemy(app)

def connect_db():
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv

def get_db():
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()

def init_db():
	with app.app_context():
		db = get_db()
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

@app.route('/')
def home():
	return render_template('home.html')

def check_email(email):
	return re.match(r'[^@]+@[^@]+\.[^@]+', email)

@app.route('/subscribe', methods=['POST'])
def subscribe_email():
	db = get_db()
	if check_email(request.form['email']):
		db.execute('insert into entries (name, email) values (?, ?)',
					[request.form['name'], request.form['email']])
		db.commit()
		flash('Thank you for your subscription!')
	else:
		flash('Invalid email address')
	return redirect(url_for('home'))

@app.route('/emails', methods=['GET'])
def show_emails():
	db = get_db()
	cur = db.execute('select name, email from entries order by id desc')
	entries = cur.fetchall()
	return render_template('show_emails.html', entries=entries)

if __name__ == '__main__':
	init_db()
	app.run()

