from werkzeug.exceptions import NotFound, Forbidden

from db import db
from managers.auth import auth
from managers.recipe import RecipeManager
from models import CommentModel


class CommentManager:

    @staticmethod
    def get_comment(comment_id):
        comment = (db.session.execute(db.select(CommentModel)
                                      .filter_by(id=comment_id)).scalar())

        if not comment:
            raise NotFound("Comment Not Found")

        return comment

    @staticmethod
    def get_comment_user(comment_user_id):

        user = auth.current_user()

        if user.id != comment_user_id:
            raise Forbidden("You are not authorized to edit this comment")

    @staticmethod
    def get_recipe_comments(recipe_id):
        recipe = RecipeManager.get_recipe(recipe_id)
        recipe_comments = recipe.comments
        return recipe_comments

    @staticmethod
    def comment_recipe(recipe_id, data):
        data['recipe_id'] = recipe_id
        current_user = auth.current_user()
        data['user_id'] = current_user.id

        new_comment = CommentModel(**data)
        db.session.add(new_comment)
        db.session.flush()

        return new_comment

    @staticmethod
    def update_comment(comment_id, data):

        comment = CommentManager.get_comment(comment_id)
        CommentManager.get_comment_user(comment.user_id)

        db.session.execute(
            db.update(CommentModel)
            .where(CommentModel.id == comment.id)
            .values(description=data['description'])
        )

        return comment

    @staticmethod
    def delete_comment(comment_id):
        comment = CommentManager.get_comment(comment_id)
        CommentManager.get_comment_user(comment.user_id)

        db.session.delete(comment)
        db.session.flush()

        return comment
