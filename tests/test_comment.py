from models.comments import CommentModel
from schemas.response.comment import ResponseCommentSchema
from tests.base import APIBaseTestCase
from tests.factories import UserFactory


class TestComment(APIBaseTestCase):

    def test_create_recipe(self):
        self.create_comment()

    def test_nonexisting_comment_and_recipe(self):
        comment, recipe, headers = self.create_comment()
        data = {}

        endpoints = (
            ("PUT", f"/recipe/{recipe.id + 1}/comment/{comment.id}"),
            ("DELETE", f"/recipe/{recipe.id + 1}/comment/{comment.id}")
        )

        for method, url in endpoints:
            resp = self.make_request(method, url, headers=headers, data=data)

            self.assertEqual(resp.status_code, 404)
            expected_message = {"message": "Recipe with this comment does not exist"}
            self.assertEqual(resp.json, expected_message)

    def test_update_delete_recipe_comment_other_user(self):
        comment, recipe, comment_user_headers = self.create_comment()
        other_user = UserFactory()
        headers = self.return_authorization_headers(other_user)

        endpoints = (
            ("PUT", f"/recipe/{recipe.id}/comment/{comment.id}"),
            ("DELETE", f"/recipe/{recipe.id}/comment/{comment.id}")
        )

        data = {
            "description": "Other description"
        }

        for method, url in endpoints:
            resp = self.make_request(method, url, headers=headers, data=data)

            self.assertEqual(resp.status_code, 403)

            expected_message = {"message": "You are not authorized to edit this comment"}
            self.assertEqual(resp.json, expected_message)

            comments = CommentModel.query.all()
            self.assertEqual(len(comments), 1)
            self.assertNotEqual(comments[0].description, "Other description")

    def test_nonexisting_comment(self):
        comment, recipe, comment_user_headers = self.create_comment()

        endpoints = (
            ("PUT", f"/recipe/{recipe.id}/comment/{comment.id + 1}"),
            ("DELETE", f"/recipe/{recipe.id}/comment/{comment.id + 1}")
        )

        data = {
            "description": "Other description"
        }

        for method, url in endpoints:
            resp = self.make_request(method, url, headers=comment_user_headers, data=data)

            self.assertEqual(resp.status_code, 404)

            expected_message = {"message": "Comment Not Found"}
            self.assertEqual(resp.json, expected_message)

            comments = CommentModel.query.all()
            self.assertEqual(len(comments), 1)
            self.assertNotEqual(comments[0].description, "Other description")

    def test_update_recipe_comment(self):
        comment, recipe, comment_user_headers = self.create_comment()

        data = {
            "description": "Other description"
        }
        resp = self.client.put(f"/recipe/{recipe.id}/comment/{comment.id}", headers=comment_user_headers, json=data)

        self.assertEqual(resp.status_code, 200)

        comments = CommentModel.query.all()
        self.assertEqual(len(comments), 1)

        expected_message = ResponseCommentSchema().dump(comments[0])
        self.assertEqual(resp.json, expected_message)
        self.assertEqual(comments[0].description, "Other description")

    def test_delete_recipe_comment(self):
        comment, recipe, comment_user_headers = self.create_comment()

        resp = self.client.delete(f"/recipe/{recipe.id}/comment/{comment.id}", headers=comment_user_headers)

        self.assertEqual(resp.status_code, 200)

        comments = CommentModel.query.all()
        self.assertEqual(len(comments), 0)

        expected_message = "Comment has been deleted"
        self.assertEqual(resp.json, expected_message)
