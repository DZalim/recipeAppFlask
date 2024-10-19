from marshmallow import Schema, fields, validates_schema, ValidationError
from marshmallow_enum import EnumField

from db import db
from models import RecipeDifficultyLevel, CategoryModel
from schemas.base import BaseRecipeSchema


class RequestRecipeSchema(BaseRecipeSchema):
    pass


class RecipeUpdateRequestSchema(Schema):
    category_id = fields.Integer(required=False)
    difficulty_level = EnumField(RecipeDifficultyLevel, by_value=True, required=False)

    @validates_schema
    def validate_category_id(self, data, **kwargs):
        if data.get("category_id"):
            category = (db.session.execute(db.select(CategoryModel)
                                           .filter_by(id=data["category_id"])).scalar())
            if not category:
                raise ValidationError("Category Not Found")

class RecipeUpdate2RequestSchema(Schema):
    recipe_name = fields.String(required=False)
    recipe_photo_url = fields.URL(required=False)
    portions = fields.Integer(required=False)
    preparing_time_in_minutes = fields.Integer(required=False)
    cooking_time_in_minutes = fields.Integer(required=False)
    ingredients = fields.String(required=False)
    description = fields.String(required=False)
