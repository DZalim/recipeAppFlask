from marshmallow import fields

from schemas.base import BaseCategorySchema


class CategoryResponseSchema(BaseCategorySchema):
    id = fields.Integer(required=True)
    created_at = fields.Date(required=True)
