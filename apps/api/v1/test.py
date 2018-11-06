from flask import request
from flask_restful import Resource
from apps.libs.http import identify_token

class Hello(Resource):
    # @identify_token(request)
    def get(self):
        return "hello word!"