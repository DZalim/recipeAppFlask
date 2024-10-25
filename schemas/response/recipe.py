from marshmallow import fields

from schemas.base.mixin import DateTimeSchema
from schemas.base.recipe import BaseRecipeSchema


class ResponseRecipeSchema(BaseRecipeSchema, DateTimeSchema):
    id = fields.Integer(required=False)
    user_id = fields.Integer(required=False)
