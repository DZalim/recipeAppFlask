from flask import request
from flask_restful import Resource

from helpers.decorators import validate_schema, validate_existing_comment_and_recipe
from managers.auth import auth
from managers.comment import CommentManager
from schemas.request.comment import RequestCommentSchema
from schemas.response.comment import ResponseCommentSchema


class RecipeComments(Resource):

    @staticmethod
    def get(recipe_pk):
        comments = CommentManager.get_recipe_comments(recipe_pk)
        return ResponseCommentSchema(many=True).dump(comments) if comments \
            else "No comments have been added to this recipe yet"

    @staticmethod
    @auth.login_required
    @validate_schema(RequestCommentSchema)
    def post(recipe_pk):
        data = request.get_json()
        comment = CommentManager.comment_recipe(recipe_pk, data)

        return ResponseCommentSchema().dump(comment)


class RecipeCommentUpdateDelete(Resource):
    @staticmethod
    @auth.login_required
    @validate_existing_comment_and_recipe
    def put(recipe_pk, comment_pk):
        data = request.get_json()
        updated_comment = CommentManager.update_comment(comment_pk, data)

        return ResponseCommentSchema().dump(updated_comment)

    @staticmethod
    @auth.login_required
    @validate_existing_comment_and_recipe
    def delete(recipe_pk, comment_pk):
        CommentManager.delete_comment(comment_pk)
        return "Comment has been deleted"
