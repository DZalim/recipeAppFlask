from flask import request
from flask_restful import Resource

from managers.user import UserManager


class RegisterUser(Resource):

    @staticmethod
    def post():
        data = request.get_json()
        token = UserManager.register(data)
        return {"token": token}, 201
