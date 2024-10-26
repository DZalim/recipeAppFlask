from marshmallow import Schema, fields, validates_schema, ValidationError, validates, validate

from db import db
from helpers.validators import validate_password, validate_spaces_factory
from models import UserModel


class BaseUserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(
        required=True,
        validate=validate.And(
            validate.Length(min=8, max=20),
            validate_password
        )
    )

    @validates('email')
    def validate_email(self, value):
        user = (db.session.execute(db.select(UserModel)
                                   .filter_by(email=value)).scalar())

        if user:
            raise ValidationError("A user with the same email already exists. "
                                  "Could it be that you disabled your account? "
                                  "Please use a different email address "
                                  "or click Forgot Password"
                                  )


class UserPersonalInfoSchema(Schema):
    first_name = fields.String(
        validate=validate.And(
            validate.Length(min=3, max=15),
            validate_spaces_factory("First Name"))
    )
    last_name = fields.String(
        validate=validate.And(
            validate.Length(min=3, max=15),
            validate_spaces_factory("Last Name"))
    )
    phone = fields.String(validate=validate.Length(min=10))

    @validates_schema
    def validate_required_fields(self, data, **kwargs):

        if self.context.get("request_type") == "create":
            required_fields = ["first_name", "last_name"]
            missing = [field for field in required_fields if field not in data]
            if missing:
                raise ValidationError(f"Missing required fields: {', '.join(missing)}")
