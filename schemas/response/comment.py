from marshmallow import fields

from schemas.base import BaseCommentSchema


class ResponseCommentSchema(BaseCommentSchema):
    comment_id = fields.Integer()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    user_id = fields.Integer()
    recipe_id = fields.Integer()
