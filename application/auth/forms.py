from flask_wtf import FlaskForm

from wtforms import StringField
from wtforms import PasswordField
from wtforms import IntegerField
from wtforms import SubmitField
from wtforms import BooleanField
from wtforms import TextAreaField
from wtforms import SelectField
from wtforms import DateField

from flask_wtf.file import FileField
from flask_wtf.file import FileAllowed

from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import NumberRange
from wtforms.validators import ValidationError

from flask_login import current_user
from application.models import User


class RegistrationForm(FlaskForm):
    first_name = StringField(
        'First Name',
        validators = [
            DataRequired(),
            Length(min=2, max=20)
        ]
    )

    last_name = StringField(
        'Last Name',
        validators = [
            DataRequired(),
            Length(min=2, max=20)
        ]
    )

    email = StringField(
        'Email',
        validators = [
            DataRequired(),
            Email()
        ]
    )

    phone = IntegerField(
        'Phone',
        validators = [
            DataRequired()
        ]
    )

    password = PasswordField(
        'Password',
        validators = [ 
            DataRequired(), 
            Length(min=6) 
        ]
    )

    confirm_password = PasswordField(
        'Confirm Password',
        validators = [
            DataRequired(),
            EqualTo('password')
        ]
    )

    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        getuseremail = email.data.strip()
        if getuseremail:
            user_email = User.query.filter_by(email=email.data).first()
            if user_email and user_email is not None:
                raise ValidationError('That email is taken. Please choose a different one.')


class RegistrationStaffForm(FlaskForm):
    username = StringField(
        'Username',
        validators = [
            DataRequired(),
            Length(min=2, max=20)
        ]
    )

    phone = StringField(
        'Phone',
        validators=[
            DataRequired(),
            Length(min=10, max=15)
        ]
    )

    email = StringField(
        'Email',
        validators = [
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        'Password',
        validators = [ 
            DataRequired(), 
            Length(min=5) 
        ]
    )

    confirm_password = PasswordField(
        'Confirm Password',
        validators = [
            DataRequired(),
            EqualTo('password')
        ]
    )

    submit = SubmitField('Sign Up')
    
    def validate_phone(self, phone):
        getuserphone = phone.data.strip()
        if getuserphone:
            user_phone = User.query.filter_by(phone=phone.data).first()
            if user_phone and user_phone is not None:
                raise ValidationError('This Phone is alredy registerd. Please choose a different one.')

    def validate_username(self, username):
        getusername = username.data.strip()
        if getusername:
            user = User.query.filter_by(username=username.data).first()
            if user and user is not None:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        getuseremail = email.data.strip()
        if getuseremail:
            user_email = User.query.filter_by(email=email.data).first()
            if user_email and user_email is not None:
                raise ValidationError('That email is taken. Please choose a different one.')
            

class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators = [
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        'Password', 
        validators = [
            DataRequired()
        ]
    )

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')