#-*- coding=utf8 -*-
from flask import Blueprint
from flask_restful import Api
from apps.api.v1.test import Hello
from apps.api.v1.articles import CreateArticle,CreateCategory
from apps.api.v1.girls import getGirlsAlbum,getGirlsTags,getGirlsImg
from apps.models.girls import girls_tag,girls_album,girls_img


def register_views(app):
    api = Api(app)
    api.add_resource(Hello, '/hello')
    api.add_resource(CreateArticle, '/article/create')
    api.add_resource(CreateCategory, '/category/create')
    api.add_resource(getGirlsAlbum, '/girls/getAlbum')
    api.add_resource(getGirlsTags, '/girls/getTags')
    api.add_resource(getGirlsImg, '/girls/getImgs')


def create_blueprint_v1():
    '''
    注册蓝图v1
    :return:
    '''
    bp_v1 = Blueprint('v1',__name__)
    register_views(bp_v1)
    return bp_v1

