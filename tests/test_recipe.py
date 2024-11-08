import os
from unittest.mock import patch

from constant import RECIPE_PHOTOS
from db import db
from models import RecipePhotosModel
from models.enums import UserRoles
from models.recipe import RecipeModel
from schemas.response.recipe import ResponseRecipeSchema
from services.cloudinary import CloudinaryService
from tests.base import APIBaseTestCase, mock_uuid
from tests.encoded_file import encoded_file
from tests.factories import UserFactory


class TestRecipe(APIBaseTestCase):

    def test_recipe_request_schema_missing_fields(self):
        matching_user = UserFactory(username="validuser", role=UserRoles.beginner)
        headers = self.return_authorization_headers(matching_user)

        recipes = RecipeModel.query.all()
        self.assertEqual(len(recipes), 0)

        data = {}

        resp = self.client.post(f"/{matching_user.username}/recipes", headers=headers, json=data)

        self.assertEqual(resp.status_code, 400)

        expected_message = {
            "message": "Invalid fields: {'_schema': ['Missing required fields: recipe_name, portions, "
                       "preparing_time_in_minutes, cooking_time_in_minutes, ingredients, description, category_id']}"
        }
        self.assertEqual(resp.json, expected_message)

        recipes = RecipeModel.query.all()
        self.assertEqual(len(recipes), 0)

    def test_recipe_request_schema_invalid_recipe_name_field(self):
        matching_user = UserFactory(username="validuser", role=UserRoles.beginner)
        headers = self.return_authorization_headers(matching_user)

        recipes = RecipeModel.query.all()
        self.assertEqual(len(recipes), 0)

        category = self.create_category()[0]

        data = {
            "recipe_name": "L",  # invalid
            "portions": 15,
            "preparing_time_in_minutes": 20,
            "cooking_time_in_minutes": 30,
            "ingredients": "1 (20 ounce) can pineapple rings, ¼ cup water, or as needed, ½ cup unsalted butter, 1 (15.25 ounce) package white cake mix (such as Betty Crocker Super Moist), ½ cup vegetable oil, 3 large egg whites, 1 ½ cups brown sugar, 7 maraschino cherries",
            "description": "Preheat the oven to 350 degrees F (175 degrees C). Drain canned pineapple into a 1-cup measure. Add water if needed to measure 1 cup. Set aside juice and 7 pineapple rings for the cake. Set any remaining juice and rings aside for another use. Melt butter in a 10- or 11-inch cast iron skillet over medium-high heat............",
            "category_id": category.id
        }

        resp = self.client.post(f"/{matching_user.username}/recipes", headers=headers, json=data)

        self.assertEqual(resp.status_code, 400)

        expected_message = {"message": "Invalid fields: {'recipe_name': ['Shorter than minimum length 2.']}"}
        self.assertEqual(resp.json, expected_message)

        recipes = RecipeModel.query.all()
        self.assertEqual(len(recipes), 0)

    def test_recipe_create(self):
        self.create_recipe()

    @patch("uuid.uuid4", mock_uuid)
    @patch.object(CloudinaryService, "upload_photo", return_value="some.url")
    def test_create_recipe_with_photo(self, mock_photo):
        user = UserFactory(role=UserRoles.beginner)
        headers = self.return_authorization_headers(user)

        recipes = RecipeModel.query.all()
        self.assertEqual(len(recipes), 0)

        category = self.create_category()[0]

        data = {
            "recipe_name": "Lasagnia",
            "portions": 15,
            "preparing_time_in_minutes": 20,
            "cooking_time_in_minutes": 30,
            "ingredients": "1 (20 ounce) can pineapple rings, ¼ cup water, or as needed, ½ cup unsalted butter, "
                           "1 (15.25 ounce) package white cake mix (such as Betty Crocker Super Moist), "
                           "½ cup vegetable oil, 3 large egg whites, 1 ½ cups brown sugar, 7 maraschino cherries",
            "description": "Preheat the oven to 350 degrees F (175 degrees C). Drain canned pineapple into a "
                           "1-cup measure. Add water if needed to measure 1 cup. Set aside juice and 7 pineapple rings "
                           "for the cake. Set any remaining juice and rings aside for another use. Melt butter in a "
                           "10- or 11-inch cast iron skillet over medium-high heat............",
            "category_id": category.id,
            "photo": encoded_file,
            "photo_extension": "jpg"
        }

        resp = self.client.post(f"/{user.username}/recipes", headers=headers, json=data)

        self.assertEqual(resp.status_code, 201)

        recipes = RecipeModel.query.all()
        self.assertEqual(len(recipes), 1)

        recipe_photos = (db.session.execute(db.select(RecipePhotosModel)
                                            .filter_by(recipe_id=recipes[0].id)).scalars().all())

        self.assertIsInstance(recipe_photos, list)
        self.assertEqual(len(recipe_photos), 1)

        recipe_name = data["recipe_name"]
        expected_message = f"A recipe named '{recipe_name}' has been created"
        self.assertEqual(resp.json, expected_message)

        file_name = mock_uuid()
        extension = data["photo_extension"]

        path = os.path.join(RECIPE_PHOTOS, f"{file_name}.{extension}")

        mock_photo.assert_called_once_with(path, extension)

    def test_existing_user_with_nonrecipe(self):
        recipe, recipe_user_headers, user = self.create_recipe()
        updated_data = {}

        endpoints = (
            ("PUT", f"/{user.username}/recipes/{recipe.id + 1}"),
            ("DELETE", f"/{user.username}/recipes/{recipe.id + 1}"),
            ("POST", f"/{user.username}/recipes/{recipe.id + 1}/photos"),
            ("DELETE", f"/{user.username}/recipes/{recipe.id + 1}/photos/1"),
        )

        for method, url in endpoints:
            resp = self.make_request(method, url, headers=recipe_user_headers, data=updated_data)

            self.assertEqual(resp.status_code, 404)

            recipes = RecipeModel.query.all()
            self.assertEqual(len(recipes), 1)

            expected_message = {"message": "No user with this recipe"}
            self.assertEqual(resp.json, expected_message)

    def test_recipe_update_success(self):
        recipe, headers, user = self.create_recipe()

        updated_data = {
            "recipe_name": "Other Name",
            "portions": 4
        }

        resp = self.client.put(f"/{user.username}/recipes/{recipe.id}", headers=headers, json=updated_data)

        self.assertEqual(resp.status_code, 200)

        recipes = RecipeModel.query.all()
        self.assertEqual(len(recipes), 1)

        sorted_data = dict(sorted(updated_data.items()))
        fields = ", ".join(key for key in sorted_data.keys())

        expected_message = f"The fields {fields} has been updated"
        self.assertEqual(resp.json, expected_message)

    def test_recipe_delete_success(self):
        recipe, headers, user = self.create_recipe()

        resp = self.client.delete(f"/{user.username}/recipes/{recipe.id}", headers=headers)

        self.assertEqual(resp.status_code, 200)

        recipes = RecipeModel.query.all()
        self.assertEqual(len(recipes), 0)

        expected_message = f"Recipe named '{recipe.recipe_name}' has been deleted"
        self.assertEqual(resp.json, expected_message)

    def test_get_single_recipe(self):
        recipe, headers, user = self.create_recipe()

        resp = self.client.get(f"/recipe/{recipe.id}", headers=headers)

        self.assertEqual(resp.status_code, 200)

        expected_message = ResponseRecipeSchema().dump(recipe)
        self.assertEqual(resp.json, expected_message)
