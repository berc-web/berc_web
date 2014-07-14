from flask import current_app
from wtforms import SubmitField, TextField, TextAreaField, HiddenField, \
	PasswordField, StringField, validators
from wtforms.validators import Required
from flask.ext.wtf import Form
from flask.ext.wtf.file import FileField, FileRequired, FileAllowed
from flask.ext.user import current_user
from flask.ext.user.forms import password_validator, username_validator, \
	unique_username_validator, unique_email_validator


# **************************
# ** Validation Functions **
# **************************


# ***********
# ** Forms **
# ***********

class CreateThreadForm(Form):
    name = TextField(validators=[Required()])
    content = TextAreaField(validators=[Required()])
    submit = SubmitField()

class CreatePostForm(Form):
    content = TextAreaField(validators=[Required()])
    submit = SubmitField()


class EditPostForm(CreatePostForm):
    pass



# class TeamRegistrationForm(Form):




# class TeamSignUpForm(Form):




class RegisterFormWithName(Form):
	password_validator_added = False

	username = StringField('Username', validators=[
        validators.Required('Username is required'),
        unique_username_validator])
	name = TextField('Name', validators=[Required()])
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
	first_name = TextField()
	last_name = TextField()
	school = TextField()

	old_password = PasswordField('Current Password', validators=[
		validators.Required('Current Password is required'),
	])
	submit = SubmitField('Update Profile')

	def validate(self):
		user_manager =  current_app.user_manager

		# Validate field-validators
		if not super(UpdateProfileForm, self).validate():
			return False

		# Verify current_user and current_password
		if not current_user or not user_manager.verify_password(self.old_password.data, current_user.password):
			self.old_password.errors.append(_('Old Password is incorrect'))
			return False

		# All is well
		return True

