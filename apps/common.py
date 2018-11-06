#-*- coding=utf8 -*-
from flask_restful import fields
def trueReturn(data, msg):
    return {
        "status": True,
        "data": data,
        "msg": msg
    }


def falseReturn(data, msg):
    return {
        "status": False,
        "data": data,
        "msg": msg
    }



def true_serializer(response_fields):
    return  {
        'status': fields.Boolean,
        'data': fields.Nested(response_fields),
        'msg': fields.String

    }
