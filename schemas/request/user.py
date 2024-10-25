from marshmallow import fields, Schema, validates_schema, ValidationError, validate, validates

from db import db
from helpers.validators import validate_password, validate_spaces_factory
from models import UserModel
from schemas.base.user import BaseUserSchema, UserPersonalInfoSchema
from schemas.request.photo import PhotoRequestSchema


class UserLoginSchema(BaseUserSchema):
    pass


class UserRegisterSchema(UserPersonalInfoSchema, BaseUserSchema):
    username = fields.String(
        required=True,
        validate=validate.And(
            validate.Length(min=3, max=15),
            validate_spaces_factory("Username")
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.context["request_type"] = "create"

    @validates('username')
    def validate_username(self, value):
        user = (db.session.execute(db.select(UserModel)
                                   .filter_by(username=value)).scalar())

        if user:
            raise ValidationError("A user with the same username already exists. "
                                  "Please enter another username.")


class UserInfoUpdateRequestSchema(UserPersonalInfoSchema, PhotoRequestSchema):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.context["request_type"] = "update"


class PasswordChangeSchema(Schema):
    old_password = fields.String(required=True)
    new_password = fields.String(
        required=True,
        validate=validate.And(
            validate.Length(min=8, max=20),
            validate_password
        )
    )

    @validates_schema
    def check_same_new_and_old_password(self, data, **kwargs):
        if data["old_password"] == data["new_password"]:
            raise ValidationError(
                "New password cannot be the same as the old password",
                field_names=["new_password"],
            )
