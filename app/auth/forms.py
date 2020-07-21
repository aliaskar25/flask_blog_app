from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired , Email, Length, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Login in")


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField("Username", validators=[DataRequired(), Length(1, 69),
                                                   Regexp("^[A-Za-z][A-Za-z0-9_.]*$", 0,
                                                   "Letters only numbers dots or underscores", )])
    password = PasswordField("Password", validators=[DataRequired(), 
                             EqualTo("password2", "Passwords must match")])
    password2 = PasswordField("Confirm password", validators=[DataRequired()])
    submit = SubmitField("Register")


    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("email already exists")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("username already exists")

    
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Old password", validators=[DataRequired()])
    new_password1 = PasswordField("Password", validators=[DataRequired(),
                                  EqualTo("new_password2", "Passwords must match")])
    new_password2 = PasswordField("Confirm password", validators=[DataRequired()])
    submit = SubmitField("Change password")