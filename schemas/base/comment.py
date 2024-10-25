from marshmallow import Schema, fields


class BaseCommentSchema(Schema):
    description = fields.String(required=True)
