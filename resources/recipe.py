from flask import request
from flask_restful import Resource

from helpers.decorators import permission_required, validate_schema, validate_logged_user, check_user_role
from managers.auth import auth
from managers.recipe import RecipeManager
from models.enums import UserRoles
from schemas.request.recipe import RequestRecipeSchema, RecipeUpdateRequestSchema
from schemas.response.recipe import ResponseRecipeSchema


class RecipeListCreate(Resource):

    @staticmethod
    @auth.login_required
    def get(username):
        logged_user = auth.current_user()
        recipes = RecipeManager.get_recipes(logged_user, username)

        return ResponseRecipeSchema().dump(recipes, many=True)

    @staticmethod
    @auth.login_required
    @validate_logged_user
    @permission_required(UserRoles.beginner, UserRoles.advanced)
    @validate_schema(RequestRecipeSchema)
    def post(username):
        data = request.get_json()
        user = auth.current_user()
        RecipeManager.create_recipe(data, user.id)
        recipe_name = data["recipe_name"]

        return f"Recipe with name '{recipe_name}' is created", 201


class RecipeListUpdate(Resource):
    @staticmethod
    @auth.login_required
    @check_user_role(5)
    @validate_schema(RecipeUpdateRequestSchema)
    def put(recipe_pk):
        data = request.get_json()
        recipe = RecipeManager.update_recipe_difficulty_or_category(data, recipe_pk)
        recipe_name = recipe.recipe_name

        return f"Recipe with name '{recipe_name}' is updated", 201
