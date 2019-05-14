#-*- coding=utf8 -*-
from flask import Blueprint
from flask_restful import Api
from apps.api.v1.test import Hello
from apps.api.v1.articles import CreateArticle,CreateCategory,CreateComment,getComment
from apps.api.v1.girls import getGirlsAlbum,getGirlsTags,getGirlsImg,getAllImgs
from apps.models.models import girls_tag,girls_album,girls_img


def register_views(app):
    api = Api(app)
    api.add_resource(Hello, '/hello')
    api.add_resource(CreateArticle, '/article/create2')
    api.add_resource(CreateCategory, '/category/create')
    api.add_resource(CreateComment, '/comment/create')
    api.add_resource(getGirlsAlbum, '/girls/getAlbum')
    api.add_resource(getGirlsTags, '/girls/getTags')
    api.add_resource(getGirlsImg, '/girls/getImgs')
    api.add_resource(getComment, '/article/getList2')
    api.add_resource(getAllImgs, '/girls/getAllImgs')


def create_blueprint_v1():
    '''
    注册蓝图v1
    :return:
    '''
    bp_v1 = Blueprint('v1',__name__)
    register_views(bp_v1)
    return bp_v1

