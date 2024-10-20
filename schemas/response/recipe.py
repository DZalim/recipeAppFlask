from marshmallow import fields

from schemas.base import BaseRecipeSchema


class ResponseRecipeSchema(BaseRecipeSchema):
    id = fields.Integer(required=False)
    user_id = fields.Integer(required=False)
    created_at = fields.DateTime(required=False)
    updated_at = fields.DateTime(required=False)
