from flask import request
from flask_restful import Resource

from helpers.decorators import validate_schema, validate_logged_user, validate_existing_user_with_recipe
from managers.auth import auth
from managers.photo import PhotoManager
from managers.recipe import RecipeManager
from managers.user import UserManager
from schemas.request.photo import PhotoRequestSchema
from schemas.response.photo import RecipePhotoResponseSchema, UserPhotoResponseSchema


class UserPhoto(Resource):
    @staticmethod
    @auth.login_required
    @validate_logged_user
    def get(username):
        user_id = UserManager.get_user(username).id
        photo_model = PhotoManager().get_photo(user_id, "user").first()

        return UserPhotoResponseSchema().dump(photo_model) if photo_model \
            else "No photo added"

    @staticmethod
    @auth.login_required
    @validate_logged_user
    @validate_schema(PhotoRequestSchema)
    def post(username):
        data = request.get_json()
        photo_model = UserManager.add_user_photo(username, data)

        return UserPhotoResponseSchema().dump(photo_model)

    @staticmethod
    @auth.login_required
    @validate_logged_user
    def delete(username):
        user_id = UserManager.get_user(username).id
        info = PhotoManager.delete_photo(user_id, "user")

        return info


class RecipePhotosList(Resource):
    @staticmethod
    def get(recipe_pk):
        RecipeManager.get_recipe(recipe_pk)
        recipe_photo = PhotoManager().get_photo(recipe_pk, "recipe").all()
        return RecipePhotoResponseSchema(many=True).dump(recipe_photo) if recipe_photo \
            else "No photos added"


class RecipePhotoCreate(Resource):
    @staticmethod
    @auth.login_required
    @validate_logged_user
    @validate_existing_user_with_recipe
    def post(username, recipe_pk):
        data = request.get_json()
        created_photo = RecipeManager.add_recipe_photo(data, recipe_pk)

        return RecipePhotoResponseSchema().dump(created_photo)


class RecipePhotoDelete(Resource):
    @staticmethod
    @auth.login_required
    @validate_logged_user
    @validate_existing_user_with_recipe
    def delete(username, recipe_pk, photo_pk):
        info = PhotoManager().delete_photo(recipe_pk, "recipe", photo_pk)
        return info
