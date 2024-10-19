from flask import request
from flask_restful import Resource

from helpers.decorators import permission_required, validate_schema
from managers.auth import auth
from managers.category import CategoryManager
from models import UserRoles
from schemas.request.category import CategoryRequestSchema
from schemas.response.category import CategoryResponseSchema
from schemas.response.recipe import ResponseRecipeSchema


class CategoryListCreate(Resource):

    @staticmethod
    def get():
        categories = CategoryManager.get_categories()

        category_schema = CategoryResponseSchema(many=True)
        result = category_schema.dump(categories)

        return result

    @staticmethod
    @auth.login_required
    @permission_required(UserRoles.admin)
    @validate_schema(CategoryRequestSchema)
    def post():
        data = request.get_json()
        CategoryManager.create_category(data)

        category_name = data["category_name"]

        return f"Recipe with name '{category_name}' is created", 201


class CategoryUpdateDelete(Resource):

    @staticmethod
    @auth.login_required
    @permission_required(UserRoles.admin)
    @validate_schema(CategoryRequestSchema)
    def put(category_pk):
        data = request.get_json()
        category = CategoryManager.update_category(category_pk, data)
        category_name = category.category_name

        return f"Category with id {category_pk} is updated. Category name is: {category_name}", 200

    @staticmethod
    @auth.login_required
    @permission_required(UserRoles.admin)
    def delete(category_pk):
        category = CategoryManager.delete_category(category_pk)
        category_name = category.category_name

        return f"Category with name {category_name} is deleted", 200


class CategoryRecipesList(Resource):
    @staticmethod
    def get(category_pk):
        category_recipes = CategoryManager.get_category_recipes(category_pk)

        if isinstance(category_recipes, str):
            return category_recipes, 200
        return ResponseRecipeSchema().dump(category_recipes, many=True), 200
