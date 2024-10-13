from marshmallow import fields
from marshmallow_enum import EnumField

from models.enums import RecipeDifficultyLevel
from schemas.base import BaseRecipeSchema


class ResponseRecipeSchema(BaseRecipeSchema):
    id = fields.Integer(required=True)
    difficulty_level = EnumField(RecipeDifficultyLevel, by_value=True)
    user_id = fields.Integer(required=True)
    created_at = fields.DateTime(required=True)
