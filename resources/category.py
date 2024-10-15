from flask import request
from flask_restful import Resource

from helpers.decorators import permission_required, validate_schema
from managers.auth import auth
from managers.category import CategoryManager
from models import UserRoles
from schemas.request.category import CategoryRequestSchema
from schemas.response.category import CategoryResponseSchema


class CategoryListCreate(Resource):

    @staticmethod
    def get():
        categories = CategoryManager.get_categories()

        category_schema = CategoryResponseSchema(many=True)
        result = category_schema.dump(categories)

        return result

    @auth.login_required
    @permission_required(UserRoles.admin)
    @validate_schema(CategoryRequestSchema)
    def post(self):
        data = request.get_json()
        CategoryManager.create_category(data)

        return f"Category with name '{data["category_name"]}' is created", 201
