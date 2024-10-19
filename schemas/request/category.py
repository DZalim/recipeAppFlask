from marshmallow import ValidationError, validates

from db import db
from models import CategoryModel
from schemas.base import BaseCategorySchema


class CategoryRequestSchema(BaseCategorySchema):

    @validates("category_name")
    def validate_same_category_name(self, value):
        category = (db.session.execute(db.select(CategoryModel)
                                       .filter_by(category_name=value)).scalar())

        if category:
            raise ValidationError("Тhis category already exists!")
