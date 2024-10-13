from db import db
from models import RecipeModel
from models.enums import UserRoles


class RecipeManager:

    @staticmethod
    def get_recipes(user):
        all_recipes = db.select(RecipeModel)

        if (user.role == UserRoles.beginner
                or user.role == UserRoles.advanced):
            all_recipes = all_recipes.filter_by(user_id=user.id)

        return db.session.execute(all_recipes).scalars().all()

    @staticmethod
    def create_recipe(data, user_id):
        data["user_id"] = user_id
        new_recipe = RecipeModel(**data)

        db.session.add(new_recipe)
        db.session.flush()

        return new_recipe
