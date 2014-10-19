from flask import current_app
from wtforms import SubmitField, TextField, TextAreaField, HiddenField, \
	PasswordField, StringField, SelectField, BooleanField, validators
from wtforms.validators import Required
from flask.ext.wtf import Form
from flask.ext.wtf.file import FileField, FileRequired, FileAllowed
from flask.ext.user import current_user
from flask.ext.user.forms import password_validator, username_validator, \
	unique_username_validator, unique_email_validator


# **************************
# ** Validation Functions **
# **************************

def email_validator(form, field):
    """ If email changed """
    if field.data != current_user.email:
    	unique_email_validator(form, field)

# ***********
# ** Forms **
# ***********

class RegisterFormWithName(Form):
	password_validator_added = False

	username = StringField('Username', validators=[
        validators.Required('Username is required'),
        unique_username_validator])
	fname = TextField('First Name', validators=[Required()])
	lname = TextField('Last Name', validators=[Required()])
	email = StringField('Email', validators=[
		validators.Required('Email is required'),
		validators.Email('Invalid Email'),
		unique_email_validator])
	password = PasswordField('Password', validators=[
		validators.Required('Password is required')])
	retype_password = PasswordField('Retype Password', validators=[
		validators.EqualTo('password', message='Password and Retype Password did not match')])
	submit = SubmitField('Register')

	def validate(self):
		# remove certain form fields depending on user manager config
		user_manager =  current_app.user_manager
		if not user_manager.enable_username:
			delattr(self, 'username')
		if not user_manager.enable_email:
			delattr(self, 'email')
		if not user_manager.enable_retype_password:
			delattr(self, 'retype_password')
		# Add custom username validator if needed
		if user_manager.enable_username:
			has_been_added = False
			for v in self.username.validators:
				if v==user_manager.username_validator:
					has_been_added = True
		if not has_been_added:
			self.username.validators.append(user_manager.username_validator)
		# Add custom password validator if needed
		has_been_added = False
		for v in self.password.validators:
			if v==user_manager.password_validator:
				has_been_added = True
		if not has_been_added:
			self.password.validators.append(user_manager.password_validator)
		# Validate field-validators
		if not super(RegisterFormWithName, self).validate():
		    return False
		# All is well
		return True


class UpdateProfileForm(Form):
	photo = FileField('Avatar', validators=[
			FileAllowed(['jpg', 'jpe', 'jpeg', 'png', 'gif', 'svg', 'bmp'], 'Images only!')
		])
	next = HiddenField()
	fname = TextField('First Name', validators=[Required()])
	lname = TextField('Last Name', validators=[Required()])
	school = TextField('School', validators=[Required()])
	email = StringField('Email', validators=[
		validators.Required('Email is required'),
		validators.Email('Invalid Email'),
		email_validator])
	major = TextField('Major', validators=[Required()])
	intro = TextAreaField('Short Introduction', validators=[Required()])
	location = SelectField('location',
		choices=[('US', 'United States'), ('CH', 'China')],
		validators=[Required()])

	submit = SubmitField('Update Profile')

	def validate(self):
		user_manager = current_app.user_manager

		# Validate field-validators
		if not super(UpdateProfileForm, self).validate():
			return False

		# All is well
		return True

class UploadNewsForm(Form):
	title = TextField('Title', validators=[Required()])
	next = HiddenField()
	image = FileField('Image', validators=[
			FileAllowed(['jpg', 'jpe', 'jpeg', 'png', 'gif', 'svg', 'bmp'], 'Images only!')
		])
	content = TextAreaField('Content', validators=[Required()])
	submit = SubmitField('Upload News')


class TeammateInvitationForm(Form):
	email = StringField('Email', validators=[
		validators.Email('Invalid Email')])
	username = StringField('Username')
	submit = SubmitField('Send Invitation')


class UpdateTeamInfoForm(Form):
	name = TextField("Team Name", validators=[Required()])
	idea = TextAreaField("Comptetion Idea", validators=[Required()])
	caseNumber = SelectField('Case Choice',
		choices=[(1, 'Placeholer1'), (2, 'Placeholer2'),
					(3, 'Placeholer3'), (4, 'Placeholer4')],
		validators=[Required()])
	submit = SubmitField("Update Team Information")


class CommentForm(Form):
	comment = TextAreaField("Comment", validators=[Required()])
	submit = SubmitField("Submit Comment")


class UploadCompArticleForm(Form):
	article = FileField('File', validators=[
		FileAllowed(['pdf'], 'PDF file only'),
		Required()
	])
	submit = SubmitField("Submit")


class SendNotificationForm(Form):
	notification = StringField("Notification", validators=[Required()])
	submit = SubmitField("Send Notification")


class CommentReplyForm(Form):
	reply = TextAreaField("Reply", validators=[Required()])
	submit = SubmitField("Submit Reply")

