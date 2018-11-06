#-*- coding=utf8 -*-
from apps.libs.redprint import Redprint
from apps.models.articles import Articles,Category
from apps.models.user import User
from flask import request,jsonify
from flask_restful import Resource,Api, reqparse,marshal_with,fields
from apps.common import trueReturn,falseReturn,true_serializer
import json




response_article_fields = {
    'id':fields.Integer,
    'title':fields.String,
}



class CreateArticle(Resource):
    '''
    创建文章
    '''
    @marshal_with(true_serializer(response_article_fields))
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str)
        parser.add_argument('content', type=str)
        parser.add_argument('user_id', type=int)
        parser.add_argument('category_id', type=int)
        article = parser.parse_args()
        atc = Articles(**dict(article))
        Articles.add(atc)
        return trueReturn(atc,'success')





response_category_field = {
    'name':fields.String
}

class CreateCategory(Resource):
    '''
    创建分类,目前这个版本分类做固定分类，数据库存固定字段。
    '''
    @marshal_with(true_serializer(response_category_field))
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        category = parser.parse_args()
        c= dict(category)
        ctg = Category(**c)
        Category.add(ctg)
        return trueReturn(ctg,'success')

