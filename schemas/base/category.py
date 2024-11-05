from marshmallow import Schema, fields, ValidationError, validates, validate

from db import db
from models import CategoryModel


class BaseCategorySchema(Schema):
    category_name = fields.String(
        required=True,
        validate=validate.Length(min=2)
    )

    @validates("category_name")
    def validate_same_category_name(self, value):
        category = (db.session.execute(db.select(CategoryModel)
                                       .filter_by(category_name=value)).scalar())

        if category:
            raise ValidationError("Тhis category already exists!")
