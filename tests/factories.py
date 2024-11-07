import factory

from db import db
from models import UserModel, CategoryModel, RecipeModel, RecipeDifficultyLevel, CommentModel


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


class CategoryFactory(BaseFactory):
    class Meta:
        model = CategoryModel

    id = factory.Sequence(lambda n: n)
    category_name = factory.Faker("sentence", nb_words=3)


class RecipeFactory(BaseFactory):
    class Meta:
        model = RecipeModel

    id = factory.Sequence(lambda n: n)
    recipe_name = factory.Faker("sentence", nb_words=3)
    portions = factory.Faker("random_int", min=1, max=12)
    preparing_time_in_minutes = factory.Faker("random_int", min=10, max=60)
    cooking_time_in_minutes = factory.Faker("random_int", min=10, max=120)
    ingredients = factory.Faker("sentence", nb_words=20)
    description = factory.Faker("paragraph", nb_sentences=3)
    difficulty_level = factory.Iterator(
        [RecipeDifficultyLevel.easy, RecipeDifficultyLevel.medium, RecipeDifficultyLevel.hard])
    # category_id = factory.SubFactory("tests.factories.CategoryFactory")
    # user_id = factory.SubFactory("tests.factories.UserFactory")


class CommentFactory(BaseFactory):
    class Meta:
        model = CommentModel

    id = factory.Sequence(lambda n: n)
    description = factory.Faker("paragraph", nb_sentences=3)
