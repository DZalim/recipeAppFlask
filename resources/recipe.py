from flask import request
from flask_restful import Resource

from helpers.decorators import permission_required, validate_schema
from managers.auth import auth
from managers.recipe import RecipeManager
from models.enums import UserRoles
from schemas.request.recipe import RequestRecipeSchema
from schemas.response.recipe import ResponseRecipeSchema


class RecipeListCreate(Resource):

    @auth.login_required
    def get(self):
        user = auth.current_user()
        recipes = RecipeManager.get_recipes(user)

        return ResponseRecipeSchema().dump(recipes, many=True)

    @auth.login_required
    @permission_required(UserRoles.beginner, UserRoles.advanced)
    @validate_schema(RequestRecipeSchema)
    def post(self):
        data = request.get_json()
        user = auth.current_user()
        RecipeManager.create_recipe(data, user.id)

        return f"Recipe with name '{data["recipe_name"]}' is created", 201
