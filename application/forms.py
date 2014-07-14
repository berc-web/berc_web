from flask import current_app
from wtforms import SubmitField, TextField, TextAreaField, HiddenField, \
	PasswordField, StringField, validators
from wtforms.validators import Required
from flask.ext.wtf import Form
from flask.ext.wtf.file import FileField, FileRequired, FileAllowed
from flask.ext.user import current_user


# **************************
# ** Validation Functions **
# **************************

def unique_email_validator(form, field):
    """ Username must be unique"""
    user_manager =  current_app.user_manager
    if not user_manager.email_is_available(field.data):
        raise ValidationError(_('This Email is no longer available. Please try another one.'))


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

