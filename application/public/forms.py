from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms import SelectField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import Regexp

class AppointmentForm(FlaskForm):
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
        'Location', 
        choices=[
            ('kolkata-airport-area', 'Kolkata Airport Area'), 
            ('habra', 'Habra'), 
            ('bongaon', 'Bongaon')
        ], 
        validators=[ 
            DataRequired()
        ]
    )
    
    submit = SubmitField('Make Appointment')



class BookTestForm(FlaskForm):
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
            DataRequired(), 
            # Regexp(r'^\+91[7-9]{2}-[0-9]{3}-[0-9]{4}$')
        ]
    )
    
    test_name = SelectField(
        'Test Name', 
        choices=[
            ('ncv', 'NCV'), 
            ('eeg', 'EEG'), 
            ('baer', 'BAER')
        ], 
        
        validators=[DataRequired()]
    )
    
    submit = SubmitField('Book Test')