#-*- coding=utf8 -*-
from apps.libs.redprint import Redprint
from apps.models.models import girls_album,girls_tag,girls_img,User
from flask import request,jsonify
from flask_restful import Resource,Api, reqparse,marshal_with,fields
from apps.common import trueReturn,falseReturn,true_serializer
from apps.libs.http import identify_token
import math
import json






response_album_fields = {
    'id':fields.Integer(attribute="albumId"),
    'girls_tag_id':fields.Integer,
    'title':fields.String,
    'cover_img':fields.String
}

response_pageInfo = {
    'pageIndex':fields.Integer,
    'pageSize':fields.Integer,
    'count':fields.Integer,
    'totalPage':fields.Integer,
}

response_album = {
    'list':fields.List(fields.Nested(response_album_fields)),
    'pageInfo':fields.Nested(response_pageInfo)

}

class getGirlsAlbum(Resource):
    @marshal_with(true_serializer(response_album))
    def get(self):
        '''
        获取相册集合
        tagID(可选):int//标签id
        keywords(可选):str//查询关键词
        pageIndex(可选):int//当前页数(默认为1)
        pageSize(可选):int//每页条数(默认为10)
        :return:
        '''
        #注册入参
        parser = reqparse.RequestParser()
        parser.add_argument('tagID',type=int,location='headers')
        parser.add_argument('keywords',type=str,location='headers')
        parser.add_argument('pageIndex',type=int,location='headers')
        parser.add_argument('pageSize',type=int,location='headers')
        #获取入参
        args = parser.parse_args()
        pageIndex = args['pageIndex'] or 1
        pageSize = args['pageSize'] or 10
        tagID = args['tagID']
        keywords = args['keywords']
        #查询参数可选
        filter = []
        if tagID:
            filter.append(girls_album.girls_tag_id==tagID)
        if keywords:
            filter.append(girls_album.title.ilike("%"+keywords+"%"))
        # album = girls_album.query.filter_by(girls_tag_id=696).first()
        search_album = girls_album.query.filter(*filter).order_by(girls_album.id.desc())
        album = search_album.paginate(pageIndex,per_page=pageSize,error_out=False)
        count = search_album.count()
        totalPage = math.floor(count/pageSize)
        return trueReturn({
            'list':album.items,
            'pageInfo':{
                'pageIndex': pageIndex,
                'pageSize': pageSize,
                'count': count,
                'totalPage': totalPage,
            }
        },'success')


response_tags = {
    'list':fields.List(fields.Nested({
        'id':fields.Integer,
        'title':fields.String,
        'tag':fields.String,
    }))

}

class getGirlsTags(Resource):
    '''
    返回图片标签
    '''

    @marshal_with(true_serializer(response_tags))
    def get(self):
        '''
        整个标签集合
        :return:
        '''
        tags = girls_tag.query.all()
        return trueReturn({
            'list':tags
        },'success')



response_imgs = {
    'list':fields.List(fields.Nested({
        'id':fields.Integer,
        'girls_album_id':fields.Integer,
        'img_url':fields.String
    })),
    'info':fields.Nested({
        'count':fields.Integer
    })
}

class getGirlsImg(Resource):
    '''
    返回图片集合
    albumId(必填): int // 相册id
    '''
    @marshal_with(true_serializer(response_imgs))
    def get(self):

        '''
        返回对应相册的图集
        :return:

        '''
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('albumId',type=int,location="headers")
            args=parser.parse_args()
            album_id = args['albumId']
            imgs = girls_img.query.filter_by(girls_album_id=album_id)
            count = girls_img.query.filter_by(girls_album_id=album_id).count()
            return trueReturn({
                'list':imgs,
                'info':{
                    'count':count
                }
            },'success')

        except Exception as e:
            print(e)
            return falseReturn('',e)







