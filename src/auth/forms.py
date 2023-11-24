from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from src.auth.models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        name='username',
        validators=[
            DataRequired(message='Field cannot be empty'),
            Length(
                min=5,
                max=50,
                message='Username must be 5 to 50 characters long'
            )
        ]
    )
    password = PasswordField(
        'Password',
        name='password',
        validators=[
            DataRequired(message='Field cannot be empty'),
            Length(
                min=8,
                max=128,
                message='Password must be minimum 8 characters long'
            )
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        name='confirm-password',
        validators=[
            DataRequired(message='Field cannot be empty'),
            EqualTo('password', message='Passwords don\'t match')
        ]
    )
    submit = SubmitField('Register', name='submit')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(
                'Username is already taken. Please choose another.'
            )


class LoginForm(FlaskForm):
    username = StringField('Username', name='username', validators=[
        DataRequired(message='Field cannot be empty')])
    password = PasswordField('Password', name='password', validators=[
        DataRequired(message='Field cannot be empty')])
    submit = SubmitField('Login', name='submit')
