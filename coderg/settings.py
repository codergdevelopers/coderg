import os 

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_TRACK_MODIFICATIONS = False

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = '465'
MAIL_USE_SSL = True
MAIL_USERNAME = 'noreply.coderg@gmail.com'
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
