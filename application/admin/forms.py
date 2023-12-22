from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, DateField, IntegerField, SelectField, SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Optional
from application.models import User

class NewUserForm(FlaskForm):
    first_name = StringField(
        'First Name', 
        validators=[
            DataRequired()
        ]
    )

    last_name = StringField(
        'Last Name', 
        validators=[
            DataRequired()
        ]
    )

    email = StringField(
        'Email', 
        validators=[
            DataRequired(), 
            Email()
        ]
    )

    phone = IntegerField(
        'Phone', 
        validators=[
            DataRequired()
        ]
    )

    password = PasswordField(
        'Password', 
        validators=[
            DataRequired()
        ]
    )

    confirm_password = PasswordField(
        'Re-type Password',
        validators = [
            DataRequired(),
            EqualTo('password')
        ]
    )

    submit = SubmitField('Add New Staff')
    

    def validate_email(self, email):
        user_email = User.query.filter_by(email=email.data).first()
        if user_email:
            raise ValidationError('That email is taken. Please choose a different one.')


class NewStaffForm(FlaskForm):
    first_name = StringField(
        'First Name', 
        validators=[
            DataRequired()
        ]
    )

    last_name = StringField(
        'Last Name', 
        validators=[
            DataRequired()
        ]
    )

    email = StringField(
        'Email', 
        validators=[
            DataRequired(), 
            Email()
        ]
    )

    phone = IntegerField(
        'Phone', 
        validators=[
            DataRequired()
        ]
    )

    assigned_location = SelectField(
        'Assigned Location', 
        choices=[
            ('', 'Select Location'), 
            ('kolkata-airport-area', 'Kolkata Airport Area'), 
            ('habra', 'Habra'), 
            ('bongaon', 'Bongaon')
        ], 
        validators=[ 
            DataRequired()
        ]   
    )

    password = PasswordField(
        'Password', 
        validators=[
            DataRequired()
        ]
    )

    confirm_password = PasswordField(
        'Re-type Password',
        validators = [
            DataRequired(),
            EqualTo('password')
        ]
    )

    submit = SubmitField('Add New Staff')
    

    def validate_email(self, email):
        user_email = User.query.filter_by(email=email.data).first()
        if user_email:
            raise ValidationError('That email is taken. Please choose a different one.')


class EditStaffForm(FlaskForm):
    first_name = StringField(
        'First Name', 
        validators=[
            DataRequired()
        ]
    )

    last_name = StringField(
        'Last Name', 
        validators=[
            DataRequired()
        ]
    )

    email = StringField(
        'Email', 
        validators=[
            DataRequired(), 
            Email()
        ]
    )

    phone = IntegerField(
        'Phone', 
        validators=[
            DataRequired()
        ]
    )

    assigned_location = SelectField(
        'Assigned Location', 
        choices=[
            ('', 'Select Location'), 
            ('kolkata-airport-area', 'Kolkata Airport Area'), 
            ('habra', 'Habra'), 
            ('bongaon', 'Bongaon')
        ], 
        validators=[ 
            Optional()
        ]   
    )

    password = PasswordField(
        'Password'
    )

    confirm_password = PasswordField(
        'Re-type Password'
    )

    submit = SubmitField('Update Staff Profile')


################################
# EDIT BOOKED TEST
################################
class EditBookedTestForm(FlaskForm):
    patient_name = StringField(
        'Paitient Name'
    )
    email = StringField(
        'Email', 
        validators=[Email()]
    )
    
    appointment_date = DateField(
        'New Test Date',
        validators=[Optional()]
    )
    
    phone = StringField(
        'Phone'
    )
    
    test_name = SelectField(
        'New Test Name', 
        choices=[
            ('ncv', 'NCV'), 
            ('eeg', 'EEG'), 
            ('baer', 'BAER')
        ]
    )
    
    report = FileField(
        'Report',
        validators = [
            FileAllowed(['jpg', 'png', 'webp', 'jpeg', 'pdf'])
        ]
    )

    submit = SubmitField('Update Test Details')


################################
# EDIT APPOINTMENTS FORM
################################
class EditAppointmentsForm(FlaskForm):
    first_name = StringField(
        'First Name', 
        validators=[
            DataRequired()
        ]
    )

    last_name = StringField(
        'Last Name', 
        validators=[
            DataRequired()
        ]
    )

    phone = StringField(
        'Phone',
        validators=[ 
            DataRequired()
        ] 
    )

    location = SelectField(
        'New Location', 
        choices=[
            ('', 'Select Location'), 
            ('kolkata-airport-area', 'Kolkata Airport Area'), 
            ('habra', 'Habra'), 
            ('bongaon', 'Bongaon')
        ], 
        validators=[ 
            Optional()
        ]   
    )

    prescription = FileField(
        'Prescription',
        validators = [
            FileAllowed(['jpg', 'png', 'webp', 'jpeg', 'pdf'])
        ]
    )

    submit = SubmitField('Upload Prescription')