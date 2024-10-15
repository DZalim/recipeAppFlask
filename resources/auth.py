from flask import request
from flask_restful import Resource

from helpers.decorators import validate_schema
from managers.auth import AuthManager, auth
from managers.user import UserManager
from schemas.request.user import UserLoginSchema, UserRegisterSchema, PasswordChangeSchema


class RegisterUser(Resource):

    @staticmethod
    @validate_schema(UserRegisterSchema)
    def post():
        data = request.get_json()
        token = UserManager.register(data)

        return {"token": token}, 201


class LoginUser(Resource):

    @staticmethod
    @validate_schema(UserLoginSchema)
    def post():
        data = request.get_json()
        token = UserManager.login(data)

        return {"token": token}, 200


class ChangePassword(Resource):

    @auth.login_required
    @validate_schema(PasswordChangeSchema)
    def put(self, username):
        data = request.get_json()
        UserManager.change_password(username, data)

        return "Password has changed"
