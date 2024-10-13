from marshmallow import Schema, fields

class BaseRecipeSchema(Schema):
    recipe_name = fields.String(required=True)
    recipe_photo_url = fields.URL(required=False)
    portions = fields.Integer(required=True)
    preparing_time_in_minutes = fields.Integer(required=True)
    cooking_time_in_minutes = fields.Integer(required=True)
    ingredients = fields.String(required=True)
    description = fields.String(required=True)
    category_id = fields.Integer(required=True)


class BaseUserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)
