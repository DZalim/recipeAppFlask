from flask import request
from flask_restful import Resource

from helpers.decorators import validate_schema
from managers.user import UserManager
from schemas.request.user import UserRegisterSchema


class RegisterUser(Resource):

    @staticmethod
    @validate_schema(UserRegisterSchema)
    def post():
        data = request.get_json()
        token = UserManager.register(data)

        return {"token": token}, 201


class LoginUser(Resource):

    @staticmethod
    def post():
        data = request.get_json()
        token = UserManager.login(data)

        return {"token": token}, 200
