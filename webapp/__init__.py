from os import environ
from flask_bootstrap import Bootstrap
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

class Config:
    # общие
    FLASK_DEBUG = environ.get('FLASK_DEBUG', '1')

    # БД
    SQLALCHEMY_DATABASE_URI = environ.get(
        'SQLALCHEMY_DATABASE_URI',
        'postgresql://postgres:111@localhost/havepaws')
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get(
        'SQLALCHEMY_TRACK_MODIFICATIONS', True)
    SQLALCHEMY_ECHO = environ.get(
        'SQLALCHEMY_ECHO', True
    )

    # формы
    SECRET_KEY = 'zzzzzzz11111'

#UPLOAD_FOLDER ='\\static\\uploads'
ALLOWED_EXTENSIONS = set(['txt','pdf','png','jpg','jpeg','gif'])

app = Flask(__name__,
            static_folder='static',
            template_folder='templates')

bootstrap = Bootstrap(app)
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

from webapp import models
from webapp import routes

#db.create_all()