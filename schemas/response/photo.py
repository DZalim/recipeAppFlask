from marshmallow import fields

from schemas.base.mixin import DateTimeSchema
from schemas.base.photo import PhotoBaseSchema


class PhotoResponseSchema(PhotoBaseSchema, DateTimeSchema):
    id = fields.Integer(required=False)
    photo_url = fields.URL(required=False)


class UserPhotoResponseSchema(PhotoResponseSchema):
    user_id = fields.Integer(required=False)


class RecipePhotoResponseSchema(PhotoResponseSchema):
    recipe_id = fields.Integer(required=False)
