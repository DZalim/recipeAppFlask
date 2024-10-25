from werkzeug.exceptions import NotFound

from db import db
from managers.photo import PhotoManager
from models.enums import UserRoles, RecipeDifficultyLevel
from models.recipe import RecipeModel
from models.user import UserModel


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

        try:
            encoded_photo = data.pop("photo")
            extension = data.pop("photo_extension")
            photo_url = PhotoManager().create_photo_url(encoded_photo, extension, "recipe")
        except KeyError:
            photo_url = None

        data["user_id"] = user_id
        new_recipe = RecipeModel(**data)
        db.session.add(new_recipe)
        db.session.flush()

        PhotoManager().create_photo(photo_url, new_recipe.id, "recipe") if photo_url else None

        return new_recipe

    @staticmethod
    def update_recipe_difficulty_or_category(data, recipe_pk):
        recipe = RecipeManager.get_recipe(recipe_pk)

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

    @staticmethod
    def add_recipe_photo(data, recipe_pk):
        photo = data["photo"]
        extension = data["photo_extension"]
        photo_url = PhotoManager().create_photo_url(photo, extension, "recipe")
        created_photo = PhotoManager().create_photo(photo_url, recipe_pk, "recipe")

        return created_photo

    @staticmethod
    def update_own_recipe(recipe_pk, data):
        recipe = RecipeManager.get_recipe(recipe_pk)

        updated_fields = []

        for key, value in data.items():
            db.session.execute(
                db.update(RecipeModel)
                .where(RecipeModel.id == recipe.id)
                .values(**{key: value})
            )

            updated_fields.append(key)

        return updated_fields

    @staticmethod
    def delete_own_recipe(recipe_pk):
        recipe = RecipeManager.get_recipe(recipe_pk)

        db.session.delete(recipe)
        db.session.flush()

        return recipe
