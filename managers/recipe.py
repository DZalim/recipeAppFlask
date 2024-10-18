from werkzeug.exceptions import NotFound

from db import db
from models import RecipeModel, UserModel
from models.enums import UserRoles


class RecipeManager:

    @staticmethod
    def get_recipes(logged_user, username):
        searched_user_recipes = (db.session.execute(
            db.select(UserModel)
            .filter_by(username=username)
        ).scalar())

        if logged_user.role == UserRoles.admin:
            recipes = (db.session.execute(
                db.select(RecipeModel)
                .filter_by(user_id=searched_user_recipes.id)
            ).scalars().all())
        else:
            if searched_user_recipes.username != logged_user.username:
                raise NotFound("Page Not Found")

            recipes = (db.session.execute(
                db.select(RecipeModel)
                .filter_by(user_id=logged_user.id)
            ).scalars().all())

        return recipes

    @staticmethod
    def create_recipe(data, user_id):
        data["user_id"] = user_id
        new_recipe = RecipeModel(**data)

        db.session.add(new_recipe)
        db.session.flush()

        return new_recipe
