from marshmallow import fields

from schemas.base.photo import PhotoBaseSchema


class PhotoRequestSchema(PhotoBaseSchema):
    photo = fields.String(required=False)
    photo_extension = fields.String(required=False)
