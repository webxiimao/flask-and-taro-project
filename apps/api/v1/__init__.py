#-*- coding=utf8 -*-
from flask import Blueprint
from flask_restful import Api
from apps.api.v1.test import Hello
from apps.api.v1.articles import CreateArticle,CreateCategory


def register_views(app):
    api = Api(app)
    api.add_resource(Hello, '/hello')
    api.add_resource(CreateArticle, '/article/create')
    api.add_resource(CreateCategory, '/category/create')


def create_blueprint_v1():
    '''
    注册蓝图v1
    :return:
    '''
    bp_v1 = Blueprint('v1',__name__)
    register_views(bp_v1)
    return bp_v1

