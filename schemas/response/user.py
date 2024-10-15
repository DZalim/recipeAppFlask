from marshmallow import fields
from marshmallow_enum import EnumField

from models.enums import UserRoles
from schemas.request.user import UserInfoRequestSchema


class UserInfoResponse(UserInfoRequestSchema):
    email = fields.Email(required=True)
    username = fields.String(required=True)
    role = EnumField(UserRoles, by_value=True)
