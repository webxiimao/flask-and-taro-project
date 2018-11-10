#-*- coding:utf8 -*-
from flask import Flask, request

from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



flask_app = Flask(__name__)

#sql配置
flask_app.config['SECRET_KEY'] = Config.SECRET_KEY
flask_app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS


@flask_app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response


db = SQLAlchemy(flask_app)
migrate = Migrate(flask_app, db)

from apps import register_blueprints

def init_app(app):
    register_blueprints(app)

init_app(flask_app)

'''
设置日志
'''
if flask_app.debug is not True:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('python.log', maxBytes=1024 * 1024 * 100, backupCount=20)
    file_handler.setLevel(logging.ERROR)
    flask_app.logger.addHandler(file_handler)

    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))

    @flask_app.errorhandler(500)
    def internal_error(exception):
        flask_app.logger.error(exception)


if __name__ == '__main__':
    flask_app.config['DEBUG'] = True
    flask_app.run()
