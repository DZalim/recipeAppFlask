from flask import request
from flask_restful import Resource

from helpers.decorators import permission_required, validate_schema
from managers.auth import auth
from managers.category import CategoryManager
from models.enums import UserRoles
from schemas.request.category import CategoryRequestSchema
from schemas.response.category import CategoryResponseSchema
from schemas.response.recipe import ResponseRecipeSchema


class CategoryListCreate(Resource):

    @staticmethod
    def get():
        categories = CategoryManager.get_categories()
        return CategoryResponseSchema(many=True).dump(categories), 200

    @staticmethod
    @auth.login_required
    @permission_required(UserRoles.admin)
    @validate_schema(CategoryRequestSchema)
    def post():
        data = request.get_json()
        new_category = CategoryManager.create_category(data)

        return f"A category named '{new_category.category_name}' has been created", 201


class CategoryUpdateDelete(Resource):

    @staticmethod
    @auth.login_required
    @permission_required(UserRoles.admin)
    @validate_schema(CategoryRequestSchema)
    def put(category_pk):
        data = request.get_json()
        category = CategoryManager.update_category(category_pk, data)

        return f"Category with id {category.id} has been updated. Category name is now: {category.category_name}", 200

    @staticmethod
    @auth.login_required
    @permission_required(UserRoles.admin)
    def delete(category_pk):
        category = CategoryManager.delete_category(category_pk)

        return f"Category named '{category.category_name}' has been deleted", 200


class CategoryRecipesList(Resource):
    @staticmethod
    def get(category_pk):
        category_recipes = CategoryManager.get_category_recipes(category_pk)

        if isinstance(category_recipes, str):
            return category_recipes, 200

        return ResponseRecipeSchema().dump(category_recipes, many=True), 200
