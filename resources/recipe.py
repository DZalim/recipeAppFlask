from flask import request
from flask_restful import Resource

from helpers.decorators import permission_required, validate_schema, validate_logged_user, check_user_role, \
    validate_existing_user_with_recipe
from managers.auth import auth
from managers.recipe import RecipeManager
from models.enums import UserRoles
from schemas.base.recipe import RecipeUpdateRequestSchema
from schemas.request.recipe import CreateRecipeRequestSchema, UpdateRecipeRequestSchema
from schemas.response.recipe import ResponseRecipeSchema


class RecipeListCreate(Resource):

    @staticmethod
    @auth.login_required
    def get(username):
        logged_user = auth.current_user()
        recipes = RecipeManager.get_recipes(logged_user, username)

        return ResponseRecipeSchema().dump(recipes, many=True) if recipes \
            else f"User '{username}' has not added any recipes yet"

    @staticmethod
    @auth.login_required
    @validate_logged_user
    @permission_required(UserRoles.beginner, UserRoles.advanced)
    @validate_schema(CreateRecipeRequestSchema)
    def post(username):
        data = request.get_json()
        user = auth.current_user()
        new_recipe = RecipeManager.create_recipe(data, user.id)

        return f"A recipe named '{new_recipe.recipe_name}' has been created", 201


class RecipeUpdateDelete(Resource):

    @staticmethod
    @auth.login_required
    @validate_logged_user
    @validate_existing_user_with_recipe
    @validate_schema(UpdateRecipeRequestSchema)
    def put(username, recipe_pk):
        data = request.get_json()
        updated_fields = RecipeManager.update_own_recipe(recipe_pk, data)

        return f"The fields {', '.join(field for field in updated_fields)} has been updated", 200

    @staticmethod
    @auth.login_required
    @validate_logged_user
    @validate_existing_user_with_recipe
    def delete(username, recipe_pk):
        recipe = RecipeManager.delete_own_recipe(recipe_pk)
        return f"Recipe named '{recipe.recipe_name}' has been deleted", 200


class RecipeListUpdate(Resource):

    @staticmethod
    def get(recipe_pk):
        recipe = RecipeManager.get_recipe(recipe_pk)
        return ResponseRecipeSchema().dump(recipe)

    @staticmethod
    @auth.login_required
    @check_user_role(5)
    @validate_schema(RecipeUpdateRequestSchema)
    def put(recipe_pk):
        data = request.get_json()
        recipe = RecipeManager.update_recipe_difficulty_or_category(data, recipe_pk)

        return f"Recipe named '{recipe.recipe_name}' has been updated", 200
