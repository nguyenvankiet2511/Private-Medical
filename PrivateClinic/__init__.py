from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from urllib.parse import quote
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "hsfjrgfjwnfgwejkfnjwegnwj"
app.secret_key = "sacfasfgwgwgwgwgwegehehehehru5hrt"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/privateclinicdb?charset=utf8mb4" % quote(
    "Admin@123")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['PAGE_SIZE'] = 8
db = SQLAlchemy(app=app)

login = LoginManager(app=app)

