run:
	python run.py

clean:
	rm application/*.pyc

update:
	# must pull the latest code from github first
	alembic upgrade head