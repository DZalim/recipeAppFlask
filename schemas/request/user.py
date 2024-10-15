from marshmallow import fields, Schema, validates_schema, ValidationError

from schemas.base import BaseUserSchema


class UserLoginSchema(BaseUserSchema):
    pass


class UserRegisterSchema(BaseUserSchema):
    username = fields.String(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    phone = fields.String(required=False)


class PasswordChangeSchema(Schema):
    old_password = fields.String(required=True)
    new_password = fields.String(required=True)

    @validates_schema
    def check_same_new_and_old_password(self, data, **kwargs):

        if data["old_password"] == data["new_password"]:
            raise ValidationError(
                "New password cannot be the same as the old password",
                field_names=["new_password"],
            )

class UserInfoRequestSchema(Schema):
    first_name = fields.String(required=False)
    last_name = fields.String(required=False)
    phone = fields.String(required=False)
