from unicodedata import category
from werkzeug.exceptions import NotFound

from db import db
from models import CategoryModel


class CategoryManager:

    @staticmethod
    def get_category_by_id(category_id):
        category = (db.session.execute(db.select(CategoryModel)
                                     .filter_by(id=category_id)).scalar())

        if not category:
            raise NotFound("Category Not Found")

        return category

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

    @staticmethod
    def update_category(category_id, data):
        category = CategoryManager.get_category_by_id(category_id)

        db.session.execute(
            db.update(CategoryModel)
            .where(CategoryModel.id == category.id)
            .values(category_name=data['category_name'])
        )

        return category

    @staticmethod
    def delete_category(category_id):
        category = CategoryManager.get_category_by_id(category_id)
        db.session.delete(category)
        db.session.flush()
        return category
