from flask.ext.wtf import Form
from wtforms import SubmitField, TextField, TextAreaField
from wtforms.validators import Required
from flask.ext.wtf.file import FileField, FileRequired, FileAllowed

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



class AvatarForm(Form):
	photo = FileField('Avatar', validators=[
			FileRequired(),
			FileAllowed(['jpg', 'jpe', 'jpeg', 'png', 'gif', 'svg', 'bmp'], 'Images only!')
		])

	submit = SubmitField('Upload Avatar')
