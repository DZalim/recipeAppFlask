from marshmallow import Schema, fields, validates_schema, ValidationError, validates, validate
from marshmallow_enum import EnumField

from db import db
from helpers.validators import validate_password, validate_spaces_factory
from models import RecipeModel, RecipeDifficultyLevel, CategoryModel, UserModel


class BaseCategorySchema(Schema):
    category_name = fields.String(required=True)


class RecipeUpdateRequestSchema(Schema):
    category_id = fields.Integer(required=False)
    difficulty_level = EnumField(RecipeDifficultyLevel, by_value=True, required=False)

    @validates_schema
    def validate_category_id(self, data, **kwargs):
        if data.get("category_id"):
            category = (db.session.execute(db.select(CategoryModel)
                                           .filter_by(id=data["category_id"])).scalar())
            if not category:
                raise ValidationError("Category Not Found")


class BaseRecipeSchema(RecipeUpdateRequestSchema):
    recipe_name = fields.String()
    portions = fields.Integer()
    photo_url = fields.URL(required=False)
    preparing_time_in_minutes = fields.Integer()
    cooking_time_in_minutes = fields.Integer()
    ingredients = fields.String()
    description = fields.String()

    @validates_schema
    def validate_required_fields(self, data, **kwargs):

        if self.context.get("request_type") == "create":
            required_fields = [
                "recipe_name", "portions", "preparing_time_in_minutes", "cooking_time_in_minutes",
                "ingredients", "description", "category_id"]
            missing = [field for field in required_fields if field not in data]
            if missing:
                raise ValidationError(f"Missing required fields: {', '.join(missing)}")

    @validates("recipe_name")
    def validate_same_recipe_name(self, value):
        recipe = (db.session.execute(db.select(RecipeModel)
                                     .filter_by(recipe_name=value)).scalar())

        if recipe:
            raise ValidationError("A recipe with the same name already exists. "
                                  "Please choose another name for your recipe!")


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
                                  "Could it be that you disabled your account?")


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


class BaseCommentSchema(Schema):
    description = fields.String(required=True)
