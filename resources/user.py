from flask import request
from flask_restful import Resource

from helpers.decorators import validate_schema
from managers.auth import auth
from managers.user import UserManager
from schemas.request.user import PasswordChangeSchema
from schemas.response.user import UserInfoResponse


class ChangePassword(Resource):

    @auth.login_required
    @validate_schema(PasswordChangeSchema)
    def put(self, username):
        data = request.get_json()
        UserManager.change_password(username, data)

        return "Password has changed"


class PersonalInfo(Resource):

    @auth.login_required
    def get(self, username):
        info = UserManager.get_personal_info(username)
        return UserInfoResponse(many=True).dump(info)

    def put(self):
        pass
