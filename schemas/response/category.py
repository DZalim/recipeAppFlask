from marshmallow import fields

from schemas.base import BaseCategorySchema


class CategoryResponseSchema(BaseCategorySchema):
    id = fields.Integer(required=False)
    created_at = fields.Date(required=False)
    updated_at = fields.Date(required=False)
