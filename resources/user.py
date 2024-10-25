from flask import request
from flask_restful import Resource

from helpers.decorators import validate_schema, validate_logged_user
from managers.auth import auth
from managers.photo import PhotoManager
from managers.user import UserManager
from schemas.request.photo import PhotoRequestSchema
from schemas.request.user import PasswordChangeSchema, UserInfoUpdateRequestSchema
from schemas.response.photo import UserPhotoResponseSchema
from schemas.response.user import UserInfoResponse


class PersonalInfo(Resource):

    @staticmethod
    @auth.login_required
    @validate_logged_user
    def get(username):
        info = UserManager.get_personal_info(username)
        return UserInfoResponse().dump(info)

    @staticmethod
    @auth.login_required
    @validate_logged_user
    @validate_schema(UserInfoUpdateRequestSchema)
    def put(username):
        data = request.get_json()
        UserManager.update_user_info(username, data)

        return "Personal info has been updated"


class UserPhoto(Resource):
    @staticmethod
    @auth.login_required
    @validate_logged_user
    def get(username):
        user_id = UserManager.get_user(username).id
        photo_model = PhotoManager().get_photo(user_id, "user")

        return UserPhotoResponseSchema(many=True).dump(photo_model) if photo_model else "No photo added"

    @staticmethod
    @auth.login_required
    @validate_logged_user
    @validate_schema(PhotoRequestSchema)
    def post(username):
        data = request.get_json()
        photo_model = UserManager.add_user_photo(username, data)

        return UserPhotoResponseSchema(many=True).dump(photo_model)

    @staticmethod
    @auth.login_required
    @validate_logged_user
    def delete(username):
        user_id = UserManager.get_user(username).id
        info = PhotoManager.delete_photo(user_id, "user")

        return info


class ChangePassword(Resource):

    @staticmethod
    @auth.login_required
    @validate_logged_user
    @validate_schema(PasswordChangeSchema)
    def put(username):
        data = request.get_json()
        UserManager.change_password(data)

        return "Password has changed"


class DeactivateProfile(Resource):

    @staticmethod
    @auth.login_required
    @validate_logged_user
    def put(username):
        user = UserManager.deactivate_profile(username)

        return f"{user.username} has been deactivated"
