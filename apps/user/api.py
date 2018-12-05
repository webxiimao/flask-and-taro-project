#-*- coding=utf8 -*-
from apps.models.user import User
from flask import jsonify,request,Blueprint
from apps.auth.auths import Auth
from .. import common
import os
import re

userRoute = Blueprint('userRoute',__name__)


@userRoute.route('/register', methods=["POST"])
def register():
    email = request.form.get("email")
    username = request.form.get("username")
    nickname = request.form.get("nickname")
    password = request.form.get("password")

    msg = "参数错误"
    if username and email and nickname and password:
        if (User.query.filter_by(username=username).first() is None) and (User.query.filter_by(email=email).first() is None):
            if bool(re.match(r'\w+@\w+.com',email)):
                user = User(email = email, username = username, nickname = nickname, password = User.set_password(password))
                result = User.add(user)
                returnUser = {
                    'id': user.id,
                    'username': user.username,
                    'nickname': user.nickname,
                    'email': user.email
                }
                return jsonify(common.trueReturn(returnUser, '用户注册成功'))
        msg = "该用户已存在，请直接登录"
    return jsonify(common.falseReturn('',msg))



@userRoute.route('/login', methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if (not username or not password):
        return jsonify(common.falseReturn('','用户名或密码不能为空'))
    else:
        auth = Auth()
        return auth.authenticate(username, password)



@userRoute.route('/info', methods=["POST"])
def info():
    auth = Auth()
    result = auth.identify(request)
    if (result['status'] and result['data']):
        user = User.query.filter_by(id=result['data']).first()
        returnUser = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'nickname':user.nickname,
            'avatar':"/static/imgs/user/avatar/%s"%user.real_avatar
        }
        result = common.trueReturn(returnUser, "请求成功")
    return jsonify(result)


@userRoute.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    '''
    获取图片
    :return:
    '''
    auth = Auth()
    result_auth = auth.identify(request)#验证token
    if (result_auth['status'] and result_auth['data']):
        file = request.files['file']
        if file:
            filename = "%s.jpg"%(result_auth['data'])
            path = os.path.join(os.getcwd(),'static','imgs','user','avatar',filename)
            user = User.query.filter_by(id=result_auth['data']).first()
            user.real_avatar = filename
            user.update()
            file.save(path)
            result = {
                'filename':filename
            }
        else:
            return jsonify(common.falseReturn('', '保存失败'))

        return jsonify(common.trueReturn(result,'保存成功'))
    else:
        return jsonify(result_auth)



@userRoute.route('/logout', methods=["POST"])
def logout():
    auth = Auth()
    result = auth.kill_auth(request)
    return jsonify(result)


