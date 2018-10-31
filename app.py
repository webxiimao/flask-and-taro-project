#-*- coding:utf8 -*-
from flask import Flask

from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

flask_app = Flask(__name__)

#sql配置
flask_app.config['SECRET_KEY'] = Config.SECRET_KEY
flask_app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS


db = SQLAlchemy(flask_app)
migrate = Migrate(flask_app, db)

from apps import register_blueprints

def init_app(app):
    register_blueprints(app)

init_app(flask_app)

if __name__ == '__main__':
    flask_app.config['DEBUG'] = True
    flask_app.run()
