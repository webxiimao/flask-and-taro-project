#-*- coding=utf8 -*-
import jwt,datetime,time
from apps.user.model import User
from flask import jsonify
from apps.common import trueReturn,falseReturn
from config import Config

class Auth():
    @staticmethod
    def encode_auth_token(user_id, login_time):
        '''
        生成token
        :param user_id:int
        :param login_time:int(timestamp)
        :return: string
        '''
        try:
            payload = {
                'exp':datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=10),
                'iat':datetime.datetime.utcnow(),
                'iss':'mao',
                'data':{
                    'id':user_id,
                    'login_time':login_time
                }
            }
            return jwt.encode(payload,Config.SECRET_KEY,algorithm='HS256')
        except Exception as e:
            return e


    @staticmethod
    def decode_auth_token(auth_token):
        '''
        验证token
        :param auth_token:string
        :return:
        '''
        try:
            payload = jwt.decode(auth_token, Config.SECRET_KEY, options={'verify_exp': False})#其中verify_exp=False不设置过期时间
            if ('data' in payload and 'id' in payload['data']):
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return "Token过期"
        except jwt.InvalidTokenError:
            return "无效Token"


    def authenticate(self, username, password):
        '''
        用户登录
        :param username:
        :param password:
        :return:
        '''
        userInfo = User.query.filter_by(username=username).first()
        if userInfo is None:
            return jsonify(falseReturn('',u'用户名不存在'))
        else:
            if userInfo.check_password(userInfo._password, password):
                login_time = int(time.time())
                userInfo.login_time = login_time
                # Users.update(Users)
                userInfo.update()
                token = self.encode_auth_token(userInfo.id, login_time)
                return jsonify(trueReturn(token, u'登录成功'))
            else:
                return jsonify(falseReturn('', u'密码不正确'))


    def identify(self, request):
        """
        用户鉴权
        :return: list
        """
        auth_header = request.headers.get("mToken")
        if auth_header:
            auth_tokenArr = auth_header.split(" ")
            if (not auth_tokenArr or auth_tokenArr[0] != 'JWT' or len(auth_tokenArr) != 2):
                result = falseReturn('', u'请传递正确的验证头信息')
            else:
                auth_token = auth_tokenArr[1]
                payload = self.decode_auth_token(auth_token)
                if not isinstance(payload, str):
                    # user = User.get(payload['data']['id'])
                    user = User.query.filter_by(id=payload['data']['id']).first()
                    if (user is None):
                        result = falseReturn('', u'找不到该用户信息')
                    else:
                        if user.login_time == payload['data']['login_time']:
                            result = trueReturn(user.id, u'请求成功')
                        else:
                            result = falseReturn('', u'Token已更改，请重新登录获取')
                else:
                    result = falseReturn('', payload)
        else:
            result = falseReturn('', u'没有提供认证token')
        return result




