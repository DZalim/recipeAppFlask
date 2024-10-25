from marshmallow import Schema, fields


class DateTimeSchema(Schema):
    created_at = fields.Date(required=False)
    updated_at = fields.Date(required=False)
