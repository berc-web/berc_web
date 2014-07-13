from flask import render_template
from flask.ext.user import forms as flask_user_forms
from flask.ext.user import UserManager, tokens
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
    change_password_form            = flask_user_forms.ChangePasswordForm,
    change_username_form            = flask_user_forms.ChangeUsernameForm,
    forgot_password_form            = flask_user_forms.ForgotPasswordForm,
    login_form                      = flask_user_forms.LoginForm,
    register_form                   = flask_user_forms.RegisterForm,
    reset_password_form             = flask_user_forms.ResetPasswordForm,

    # Validators
    username_validator              = flask_user_forms.username_validator,
    password_validator              = flask_user_forms.password_validator,

    # Miscellaneous
    token_manager                   = tokens.TokenManager(),

)