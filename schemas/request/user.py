from marshmallow import fields

from schemas.base import BaseUserSchema


class UserLoginSchema(BaseUserSchema):
    pass


class UserRegisterSchema(BaseUserSchema):
    username = fields.String(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    phone = fields.String(required=False)
