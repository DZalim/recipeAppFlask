from marshmallow import fields
from marshmallow_enum import EnumField

from models.enums import UserRoles
from schemas.request.user import UserInfoUpdateRequestSchema


class UserInfoResponse(UserInfoUpdateRequestSchema):
    email = fields.Email()
    username = fields.String()
    role = EnumField(UserRoles, by_value=True)
