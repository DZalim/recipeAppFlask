from db import db
from random import randint

import factory

from models import UserModel, UserRoles, ProfileStatus


class BaseFactory(factory.Factory):
    @classmethod
    def create(cls, **kwargs):
        object = super().create(**kwargs)
        db.session.add(object)
        db.session.flush()
        return object


class UserFactory(BaseFactory):
    class Meta:
        model = UserModel

    id = factory.Sequence(lambda n: n)
    email = factory.Faker("email")
    password = factory.Faker("password")
    username = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    # the following lines have default values
        # phone = str(randint(100000, 200000))
        # role = UserRoles.beginner
        # profile_status = ProfileStatus.active

