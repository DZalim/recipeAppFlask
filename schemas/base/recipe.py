from marshmallow import Schema, fields, validates_schema, ValidationError, validates, validate
from marshmallow_enum import EnumField

from db import db
from models import RecipeModel, RecipeDifficultyLevel, CategoryModel


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
    recipe_name = fields.String(validate=validate.Length(min=2))
    portions = fields.Integer(validate=validate.Range(min=1))
    preparing_time_in_minutes = fields.Integer(validate=validate.Range(min=1))
    cooking_time_in_minutes = fields.Integer(validate=validate.Range(min=1))
    ingredients = fields.String(validate=validate.Length(min=10))
    description = fields.String(validate=validate.Length(min=10))

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
