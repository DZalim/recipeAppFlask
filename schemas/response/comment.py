from marshmallow import fields

from schemas.base.comment import BaseCommentSchema
from schemas.base.mixin import DateTimeSchema


class ResponseCommentSchema(BaseCommentSchema, DateTimeSchema):
    comment_id = fields.Integer()
    user_id = fields.Integer()
    recipe_id = fields.Integer()
