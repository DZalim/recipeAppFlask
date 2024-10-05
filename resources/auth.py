from flask import request
from flask_restful import Resource

from managers.user import UserManager


class RegisterUser(Resource):
    def post(self):
        data = request.get_json()
        user = UserManager.register(data)
        return 'User is created', 201
