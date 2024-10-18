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
