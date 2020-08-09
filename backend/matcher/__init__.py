from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
#from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from config import Config   #from config module, import config class
from flask_babel import Babel, lazy_gettext as _l
from flask_cors import CORS
from flask_jwt_extended import JWTManager



app = Flask(__name__)
#The __name__ variable passed to the Flask class is a Python predefined variable,
#which is set to the name of the module in which it is used. Flask uses the location of the module passed
#here as a starting point when it needs to load associated resources such as template files

app.config.from_object(Config) #tells flask to use and apply the config file
CORS(app)
JWTManager(app)

db = SQLAlchemy(app) #db object that represents the database.
ma = Marshmallow(app)
bcrypt = Bcrypt(app) #password hashing function
login = LoginManager(app) #initializes the flask-login extension
migrate = Migrate(app, db) #object that represents the migration engine.
babel = Babel(app)



#bootstrap = Bootstrap()

login.login_view = 'login'

from matcher import routes, models
#importing a new module called models at the bottom. This module will define the structure of the database.

def main():
    db.create_all()
