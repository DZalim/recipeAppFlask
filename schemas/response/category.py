from marshmallow import fields

from schemas.base.category import BaseCategorySchema
from schemas.base.mixin import DateTimeSchema


class CategoryResponseSchema(BaseCategorySchema, DateTimeSchema):
    id = fields.Integer(required=False)
