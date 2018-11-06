#-*- coding=utf8 -*-
from flask import  jsonify
from apps.auth.auths import Auth

'''
http模块工具
'''

def identify_token(request):
    '''
    验证token的一个装饰器
    :param func:
    :return:
    '''
    def decorator(func):
        def wrapper(*args, **kwargs):
            auth = Auth()
            result = auth.identify(request)
            if (result['status'] and result['data']):
                return func(*args, **kwargs)
            else:
                return jsonify(result)
        return wrapper
    return decorator

