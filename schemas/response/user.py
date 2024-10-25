from marshmallow import fields
from marshmallow_enum import EnumField

from models.enums import UserRoles, ProfileStatus
from schemas.base.mixin import DateTimeSchema
from schemas.base.user import UserPersonalInfoSchema


class UserInfoResponse(UserPersonalInfoSchema, DateTimeSchema):
    email = fields.Email()
    username = fields.String()
    role = EnumField(UserRoles, by_value=True)
    profile_status = EnumField(ProfileStatus, by_value=True)
