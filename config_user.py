from flask import render_template
from flask.ext.user import UserManager, forms, tokens
from application import db_adapter

def user_login():
	return render_template('flask_user/login.html')

user_manager = UserManager(
    db_adapter,
    app = None,

    # view functions
        # login_view_function           = user_login,
        # change_password_view_function = my_view_function1,
        # change_username_view_function = my_view_function2,
        # confirm_email_view_function   = my_view_function3,
        # forgot_password_view_function = my_view_function4,
        # logout_view_function          = my_view_function6,
        # register_view_function        = my_view_function7,
        # reset_password_view_function  = my_view_function8

    # Forms
    change_password_form            = forms.ChangePasswordForm,
    change_username_form            = forms.ChangeUsernameForm,
    forgot_password_form            = forms.ForgotPasswordForm,
    login_form                      = forms.LoginForm,
    register_form                   = forms.RegisterForm,
    reset_password_form             = forms.ResetPasswordForm,

    # Validators
    username_validator              = forms.username_validator,
    password_validator              = forms.password_validator,

    # Miscellaneous
    token_manager                   = tokens.TokenManager(),

)