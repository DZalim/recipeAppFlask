import os
from unittest.mock import patch

from constant import RECIPE_PHOTOS
from db import db
from models.photos import UsersPhotoModel, RecipePhotosModel
from models.user import UserModel
from schemas.response.photo import UserPhotoResponseSchema, RecipePhotoResponseSchema
from services.cloudinary import CloudinaryService
from tests.base import APIBaseTestCase, mock_uuid
from tests.encoded_file import encoded_file
from tests.factories import UserFactory


class TestUserPhoto(APIBaseTestCase):

    def test_get_user_photo_no_added(self):
        users = UserModel.query.all()
        self.assertEqual(len(users), 0)

        user = UserFactory()
        headers = self.return_authorization_headers(user)

        users = UserModel.query.all()
        self.assertEqual(len(users), 1)

        resp = self.client.get(f"/{user.username}/personal_photo", headers=headers)

        user_photo = (db.session.execute(db.select(UsersPhotoModel)
                                         .filter_by(user_id=user.id)).scalar())

        self.assertIsNone(user_photo)

        self.assertEqual(resp.status_code, 200)
        expected_message = "No photo added"
        self.assertEqual(resp.json, expected_message)

    @patch("uuid.uuid4", mock_uuid)
    @patch.object(CloudinaryService, "upload_photo", return_value="some.url")
    def test_create_user_photo(self, mock_photo):
        self.create_user_photo()

    @patch("uuid.uuid4", mock_uuid)
    @patch.object(CloudinaryService, "upload_photo", return_value="some.url")
    def test_get_user_photo_added(self, mock_photo):
        photo, user, headers = self.create_user_photo()

        resp = self.client.get(f"/{user.username}/personal_photo", headers=headers)

        users = UserModel.query.all()
        self.assertEqual(len(users), 1)

        user_photo = (db.session.execute(db.select(UsersPhotoModel)
                                         .filter_by(user_id=user.id)).scalar())

        self.assertIsNotNone(user_photo)
        self.assertIsInstance(user_photo, UsersPhotoModel)

        self.assertEqual(resp.status_code, 200)
        expected_message = UserPhotoResponseSchema().dump(user_photo)
        self.assertEqual(resp.json, expected_message)

    @patch("uuid.uuid4", mock_uuid)
    @patch.object(CloudinaryService, "upload_photo", return_value="some.url")
    def test_add_other_photo(self, mock_photo):
        photo, user, headers = self.create_user_photo()

        self.assertIsNotNone(photo)
        self.assertIsInstance(photo, UsersPhotoModel)

        photo_data = {
            "photo": encoded_file,
            "photo_extension": "jpg"
        }

        resp = self.client.post(f"/{user.username}/personal_photo", headers=headers, json=photo_data)

        users = UserModel.query.all()
        self.assertEqual(len(users), 1)

        user_photo = (db.session.execute(db.select(UsersPhotoModel)
                                         .filter_by(user_id=user.id)).scalar())

        self.assertIsNotNone(user_photo)
        self.assertIsInstance(user_photo, UsersPhotoModel)

        self.assertEqual(resp.status_code, 400)
        expected_message = {"message": "You cannot add another profile picture"}
        self.assertEqual(resp.json, expected_message)

    @patch("uuid.uuid4", mock_uuid)
    @patch.object(CloudinaryService, "upload_photo", return_value="some.url")
    @patch.object(CloudinaryService, "delete_photo", return_value="some")
    def test_delete_existing_user_photo(self, mock_photo_delete, mock_photo_upload):
        photo, user, headers = self.create_user_photo()

        resp = self.client.delete(f"/{user.username}/personal_photo", headers=headers)

        users = UserModel.query.all()
        self.assertEqual(len(users), 1)

        user_photo = (db.session.execute(db.select(UsersPhotoModel)
                                         .filter_by(user_id=user.id)).scalar())

        self.assertIsNone(user_photo)

        self.assertEqual(resp.status_code, 200)
        expected_message = "The photo has been deleted"
        self.assertEqual(resp.json, expected_message)

        mock_photo_delete.assert_called_once_with(photo.photo_url)

    def test_delete_nonexisting_user_photo(self):
        user = UserFactory()
        headers = self.return_authorization_headers(user)

        users = UserModel.query.all()
        self.assertEqual(len(users), 1)

        user_photo = (db.session.execute(db.select(UsersPhotoModel)
                                         .filter_by(user_id=user.id)).scalar())

        self.assertIsNone(user_photo)

        resp = self.client.delete(f"/{user.username}/personal_photo", headers=headers)

        self.assertEqual(resp.status_code, 200)
        expected_message = "No photo to delete"
        self.assertEqual(resp.json, expected_message)


class TestRecipePhoto(APIBaseTestCase):
    def test_get_non_existing_recipe_photos(self):
        recipe = self.create_recipe()[0]

        resp = self.client.get(f"/recipe/{recipe.id}/photos")

        recipe_photos = (db.session.execute(db.select(RecipePhotosModel)
                                            .filter_by(recipe_id=recipe.id)).scalars().all())

        self.assertIsInstance(recipe_photos, list)
        self.assertEqual(len(recipe_photos), 0)

        self.assertEqual(resp.status_code, 200)
        expected_message = "No photos added"
        self.assertEqual(resp.json, expected_message)

    @patch("uuid.uuid4", mock_uuid)
    @patch.object(CloudinaryService, "upload_photo", return_value="some.url")
    def test_create_recipe_photo(self, mock_photo):
        self.create_recipe_photo()

    @patch("uuid.uuid4", mock_uuid)
    @patch.object(CloudinaryService, "upload_photo", return_value="some.url")
    def test_get_recipe_photos_added(self, mock_photo):
        recipe, headers, user = self.create_recipe()

        for i in range(5):
            photo_data = {
                "photo": encoded_file,
                "photo_extension": "jpg"
            }

            self.client.post(f"/{user.username}/recipes/{recipe.id}/photos", headers=headers, json=photo_data)

            file_name = mock_uuid()
            extension = photo_data["photo_extension"]

            path = os.path.join(RECIPE_PHOTOS, f"{file_name}.{extension}")

            mock_photo.assert_called_with(path, extension)

        recipe_photos = (db.session.execute(db.select(RecipePhotosModel)
                                            .filter_by(recipe_id=recipe.id)).scalars().all())

        self.assertIsInstance(recipe_photos, list)
        self.assertEqual(len(recipe_photos), 5)

        resp = self.client.get(f"/recipe/{recipe.id}/photos")

        self.assertEqual(resp.status_code, 200)
        expected_message = RecipePhotoResponseSchema(many=True).dump(recipe_photos)
        self.assertEqual(resp.json, expected_message)

    @patch("uuid.uuid4", mock_uuid)
    @patch.object(CloudinaryService, "upload_photo", return_value="some.url")
    @patch.object(CloudinaryService, "delete_photo", return_value="some")
    def test_delete_existing_recipe_photo(self, mock_photo_delete, mock_photo_upload):
        recipe_photo, user, user_headers = self.create_recipe_photo()

        resp = self.client.delete(f"/{user.username}/recipes/{recipe_photo.recipe_id}/photos/{recipe_photo.id}",
                                  headers=user_headers)

        recipe_photos = (db.session.execute(db.select(RecipePhotosModel)
                                            .filter_by(recipe_id=recipe_photo.recipe_id)).scalars().all())

        self.assertIsInstance(recipe_photos, list)
        self.assertEqual(len(recipe_photos), 0)

        expected_message = "The photo has been deleted"
        self.assertEqual(resp.json, expected_message)

        mock_photo_delete.assert_called_once_with(recipe_photo.photo_url)

    def test_delete_nonexisting_recipe_photo(self):
        recipe, headers, user = self.create_recipe()

        recipe_photos = (db.session.execute(db.select(RecipePhotosModel)
                                            .filter_by(recipe_id=recipe.id)).scalars().all())

        self.assertIsInstance(recipe_photos, list)
        self.assertEqual(len(recipe_photos), 0)

        resp = self.client.delete(f"/{user.username}/recipes/{recipe.id}/photos/5", headers=headers)

        recipe_photos = (db.session.execute(db.select(RecipePhotosModel)
                                            .filter_by(recipe_id=recipe.id)).scalars().all())

        self.assertIsInstance(recipe_photos, list)
        self.assertEqual(len(recipe_photos), 0)

        self.assertEqual(resp.status_code, 200)
        expected_message = "No photo to delete"
        self.assertEqual(resp.json, expected_message)
