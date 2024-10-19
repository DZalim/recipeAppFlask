from werkzeug.exceptions import NotFound

from db import db
from models import RecipeModel, UserModel, RecipeDifficultyLevel
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
    def get_recipe(recipe_id):
        recipe = (db.session.execute(db.select(RecipeModel)
                                     .filter_by(id=recipe_id)).scalar())

        if not recipe:
            raise NotFound("Recipe Not Found")

        return recipe

    @staticmethod
    def create_recipe(data, user_id):
        data["user_id"] = user_id
        new_recipe = RecipeModel(**data)

        db.session.add(new_recipe)
        db.session.flush()

        return new_recipe

    def update_recipe_difficulty_or_category(self, data, recipe_pk):
        recipe = self.get_recipe(recipe_pk)

        if "difficulty_level" in data:
            db.session.execute(
                db.update(RecipeModel)
                .where(RecipeModel.id == recipe.id)
                .values(difficulty_level=RecipeDifficultyLevel[data["difficulty_level"]])
            )

        if "category_id" in data:
            db.session.execute(
                db.update(RecipeModel)
                .where(RecipeModel.id == recipe.id)
                .values(category_id=data["category_id"])
            )

        return recipe
