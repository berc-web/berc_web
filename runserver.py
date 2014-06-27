from application import app, db

# try:
# 	db.app = app
# 	db.init_app(app)
# 	db.create_all()
# except Exception:
# 	# pass
# 	raise Exception

db.create_all()
app.run()
