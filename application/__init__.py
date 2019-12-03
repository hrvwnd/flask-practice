from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=('mysql+pymysql://' + getenv('MYSQL_USER') + ':' + getenv('MYSQL_PASSWORD') + '@' + getenv('MYSQL_HOST') + '/' + getenv('MYSQL_DB'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
#app.config['SECRET_KEY'] = '43riu34jhferugfhrf83h98eh3fuwhergiurhe'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
from application import routes