from db import db
from models import CategoryModel


class CategoryManager:

    @staticmethod
    def get_categories():
        all_categories = db.select(CategoryModel)
        return db.session.execute(all_categories).scalars().all()

    @staticmethod
    def create_category(data):
        new_category = CategoryModel(**data)

        db.session.add(new_category)
        db.session.flush()

        return new_category
