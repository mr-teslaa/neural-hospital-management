import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

# production=True
production=False

class Config:
    SECRET_KEY='248fb9a5bdffa13c0bc136504ebf75c2'
    if production is True:
        SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI')
    else:
        SQLALCHEMY_DATABASE_URI=os.getenv('DEV_SQLALCHEMY_DATABASE_URI')

    # set optional bootswatch theme
    # FLASK_ADMIN_SWATCH = 'cerulean'
    
    # SQLALCHEMY_TRACK_MODIFICATIONS=True
    MAIL_SERVER = os.getenv('SMTP_SERVER')
    MAIL_DEFAULT_SENDER = 'example@domain.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('EMAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')