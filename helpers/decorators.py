from functools import wraps

from flask import request
from marshmallow import Schema
from werkzeug.exceptions import Forbidden, BadRequest, NotFound

from db import db
from managers.auth import auth
from managers.comment import CommentManager
from models import UserRoles, UserModel, RecipeModel


def permission_required(*required_roles):
    def decorator(func):
        def wrapper(*args, **kwargs):
            current_user = auth.current_user()
            if current_user.role not in required_roles:
                raise Forbidden("You do not have permissions to access this resource")

            return func(*args, **kwargs)

        return wrapper

    return decorator


def validate_schema(schema_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            schema: Schema = schema_name()
            data = request.get_json()
            errors = schema.validate(data)

            if errors:
                raise BadRequest(f"Invalid fields: {errors}")

            return func(*args, **kwargs)

        return wrapper

    return decorator


def validate_logged_user(func):
    @wraps(func)
    def wrapper(username, *args, **kwargs):
        current_user = auth.current_user()

        if current_user.username != username:
            raise NotFound("User not found")

        return func(username, *args, **kwargs)

    return wrapper


def check_user_role(required_num_of_recipes: int):
    def decorator(func):
        def wrapper(*args, **kwargs):
            current_user = auth.current_user()
            current_user_num_of_recipes = len(current_user.recipes)

            if current_user_num_of_recipes >= required_num_of_recipes and current_user.role == UserRoles.beginner:
                db.session.execute(db.update(UserModel)
                                   .where(UserModel.id == current_user.id)
                                   .values(role=UserRoles.advanced))

            elif current_user_num_of_recipes < required_num_of_recipes and current_user.role == UserRoles.advanced:
                db.session.execute(db.update(UserModel)
                                   .where(UserModel.id == current_user.id)
                                   .values(role=UserRoles.beginner))

            if current_user.role == UserRoles.admin:
                return func(*args, **kwargs)

            if current_user.role == UserRoles.advanced:
                data = request.get_json()
                if "category_id" in data:
                    raise Forbidden("Advanced users cannot change category_id")

                return func(*args, **kwargs)

            raise Forbidden("You do not have permissions to access this resource")  # remains a beginner user

        return wrapper

    return decorator


def validate_existing_user_with_recipe(func):
    @wraps(func)
    def wrapper(username, recipe_pk, *args, **kwargs):
        recipe_owner = (db.session.execute(db.select(UserModel)
                                           .join(UserModel.recipes)
                                           .filter(RecipeModel.id == recipe_pk))
                        .scalar())

        if not recipe_owner or recipe_owner.username != username:
            raise NotFound("No user with this recipe")

        return func(username, recipe_pk, *args, **kwargs)

    return wrapper


def validate_existing_comment_and_recipe(func):
    @wraps(func)
    def wrapper(recipe_pk, comment_pk, *args, **kwargs):
        comment = CommentManager.get_comment(comment_pk)
        if recipe_pk != comment.recipe_id:
            raise NotFound("Recipe with this comment does not exist")

        return func(recipe_pk, comment_pk, *args, **kwargs)

    return wrapper
