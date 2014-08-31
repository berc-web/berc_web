run:
	export AWS_ACCESS_KEY_ID='AKIAJIFKOR7IKUWAZM2Q'
	export AWS_SECRET_ACCESS_KEY='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'
	export S3_BUCKET_NAME='eecc2015-test'
	python run.py

clean:
	rm application/*.pyc

update:
	# must pull the latest code from github first
	alembic upgrade head