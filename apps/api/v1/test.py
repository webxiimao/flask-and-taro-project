from flask import request
from flask_restful import Resource
from apps.utils.http import identify_token

class Hello(Resource):
    @identify_token(request)
    def get(self):
        return "hello word!"