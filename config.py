#-*- coding:utf8 -*-

import os

class Config(object):
    SECRET_KEY = 'Xiimao'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@127.0.0.1:3306/flaskstudy'
    SQLALCHEMY_TRACK_MODIFICATIONS = True



