#-*- coding=utf8 -*-
from .model import User
from flask import jsonify,request,Blueprint
from apps.auth.auths import Auth
from .. import common
from app import flask_app


userRoute = Blueprint('userRoute',__name__)


@userRoute.route('/register', methods=["POST"])
def register():
    email = request.form.get("email")
    username = request.form.get("username")
    nickname = request.form.get("nickname")
    password = request.form.get("password")
    user = User(email = email, username = username, nickname = nickname, password = User.set_password(password))
    result = User.add(user)
    returnUser = {
        'id': user.id,
        'username' : user.username,
        'nickname' : user.nickname,
        'email' : user.email
    }
    return jsonify(common.trueReturn(returnUser,'用户注册成功'))



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
            'nickname':user.nickname
        }
        result = common.trueReturn(returnUser, "请求成功")
    return jsonify(result)




@userRoute.route('/logout', methods=["POST"])
def logout():
    auth = Auth()
    result = auth.kill_auth(request)
    return jsonify(result)


