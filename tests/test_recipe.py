import os
import random
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
from tests.factories import UserFactory, RecipeFactory, CategoryFactory


class TestRecipeSchemaFields(APIBaseTestCase):
    def test_recipe_request_schema_missing_fields(self):
        user = UserFactory(role=UserRoles.beginner)
        headers = self.return_authorization_headers(user)

        recipes = RecipeModel.query.all()
        self.assertEqual(len(recipes), 0)

        data = {}

        resp = self.client.post(f"/{user.username}/recipes", headers=headers, json=data)

        self.assertEqual(resp.status_code, 400)

        expected_message = {
            "message": "Invalid fields: {'_schema': ['Missing required fields: recipe_name, portions, "
                       "preparing_time_in_minutes, cooking_time_in_minutes, ingredients, description, category_id']}"
        }
        self.assertEqual(resp.json, expected_message)

        recipes = RecipeModel.query.all()
        self.assertEqual(len(recipes), 0)

    def test_recipe_request_schema_invalid_recipe_name_field(self):
        user = UserFactory(role=UserRoles.beginner)
        headers = self.return_authorization_headers(user)

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

        resp = self.client.post(f"/{user.username}/recipes", headers=headers, json=data)

        self.assertEqual(resp.status_code, 400)

        expected_message = {"message": "Invalid fields: {'recipe_name': ['Shorter than minimum length 2.']}"}
        self.assertEqual(resp.json, expected_message)

        recipes = RecipeModel.query.all()
        self.assertEqual(len(recipes), 0)


class TestUserWithRecipe(APIBaseTestCase):
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


class TestCreateRecipe(APIBaseTestCase):
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


class TestGetRecipe(APIBaseTestCase):
    def test_get_single_recipe(self):
        recipe = self.create_recipe()[0]

        resp = self.client.get(f"/recipe/{recipe.id}")

        self.assertEqual(resp.status_code, 200)

        expected_message = ResponseRecipeSchema().dump(recipe)
        self.assertEqual(resp.json, expected_message)

    def test_get_username_own_recipes_norecipe(self):
        user = UserFactory(role=UserRoles.beginner)
        headers = self.return_authorization_headers(user)

        recipes = RecipeModel.query.all()
        self.assertEqual(len(recipes), 0)

        resp = self.client.get(f"/{user.username}/recipes", headers=headers)

        self.assertEqual(resp.status_code, 200)
        expected_message = f"User '{user.username}' has not added any recipes yet"
        self.assertEqual(resp.json, expected_message)

    def test_get_username_recipes(self):
        category = self.create_category()[0]
        user = UserFactory(role=UserRoles.beginner)
        headers = self.return_authorization_headers(user)

        recipes = []
        for i in range(7):
            recipe = RecipeFactory(category_id=category.id, user_id=user.id)
            recipes.append(recipe)

        other_user = UserFactory(role=UserRoles.advanced)
        other_recipes = []
        for i in range(6):
            RecipeFactory(category_id=category.id, user_id=other_user.id)
            recipes.append(other_recipes)

        all_recipes = RecipeModel.query.all()
        self.assertEqual(len(all_recipes), 13)

        user_recipes = (db.session.execute(db.select(RecipeModel)
                                           .filter_by(user_id=user.id)).scalars().all())
        self.assertEqual(len(user_recipes), 7)

        resp = self.client.get(f"/{user.username}/recipes", headers=headers)

        self.assertEqual(resp.status_code, 200)
        expected_message = ResponseRecipeSchema().dump(user_recipes, many=True)
        self.assertEqual(resp.json, expected_message)

    def test_get_username_recipes_by_admin(self):  # have access to all users recipes
        category = self.create_category()[0]
        admin = UserFactory(role=UserRoles.admin)
        headers = self.return_authorization_headers(admin)

        user_endpoint = UserFactory(role=UserRoles.beginner)

        recipes = []
        for i in range(5):
            recipe = RecipeFactory(category_id=category.id, user_id=user_endpoint.id)
            recipes.append(recipe)
            self.assertNotEqual(recipe.user_id, admin.id)

        for i in range(5):
            user = UserFactory(role=random.choice([UserRoles.beginner, UserRoles.advanced]))
            recipe = RecipeFactory(category_id=category.id, user_id=user.id)
            recipes.append(recipe)
            self.assertNotEqual(recipe.user_id, admin.id)

        all_recipes = RecipeModel.query.all()
        self.assertEqual(len(all_recipes), 10)

        user_recipes = (db.session.execute(db.select(RecipeModel)
                                           .filter_by(user_id=user_endpoint.id)).scalars().all())
        self.assertEqual(len(user_recipes), 5)

        resp = self.client.get(f"/{user_endpoint.username}/recipes", headers=headers)

        self.assertEqual(resp.status_code, 200)
        expected_message = ResponseRecipeSchema().dump(user_recipes, many=True)
        self.assertEqual(resp.json, expected_message)


class TestUpdateRecipe(APIBaseTestCase):
    def test_own_recipe_update_success(self):
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

    def test_update_recipe_category_and_difficulty_by_admin(self):
        category = CategoryFactory()

        recipe_user = UserFactory(role=UserRoles.beginner)
        recipe = RecipeFactory(category_id=category.id, user_id=recipe_user.id)

        admin = UserFactory(role=UserRoles.admin)
        headers = self.return_authorization_headers(admin)

        other_category = CategoryFactory()

        data = {
            "category_id": other_category.id,
            "difficulty_level": "medium"
        }

        resp = self.client.put(f"/recipe/{recipe.id}", headers=headers, json=data)

        self.assertEqual(resp.status_code, 200)
        expected_message = f"Recipe named '{recipe.recipe_name}' has been updated"
        self.assertEqual(resp.json, expected_message)

    def test_update_other_recipe_category_and_difficulty_by_beginner_user(self):
        category = CategoryFactory()

        recipe_user = UserFactory(role=UserRoles.beginner)
        recipe = RecipeFactory(category_id=category.id, user_id=recipe_user.id)

        advanced_user = UserFactory(role=UserRoles.advanced)  # when there are less than 5 recipes it becomes beginner
        headers = self.return_authorization_headers(advanced_user)

        other_category = CategoryFactory()

        data = {
            "category_id": other_category.id,
            "difficulty_level": "hard"
        }

        resp = self.client.put(f"/recipe/{recipe.id}", headers=headers, json=data)

        self.assertEqual(resp.status_code, 403)
        expected_message = {
            "message": "You do not have permissions to access this resource"
        }
        self.assertEqual(resp.json, expected_message)

    def create_info(self):
        category = CategoryFactory()

        recipe_user = UserFactory(role=UserRoles.beginner)
        recipe = RecipeFactory(category_id=category.id, user_id=recipe_user.id)

        beginner_user = UserFactory(role=UserRoles.beginner)
        headers = self.return_authorization_headers(beginner_user)

        for i in range(5):  # when there are 5 recipes it becomes advanced
            RecipeFactory(category_id=category.id, user_id=beginner_user.id)

        other_category = CategoryFactory()

        return other_category, recipe, headers

    def test_update_others_recipe_category_and_difficulty_by_advanced_user(self):
        other_category, recipe, headers = self.create_info()

        data = {
            "category_id": other_category.id,
            "difficulty_level": "medium"
        }

        resp = self.client.put(f"/recipe/{recipe.id}", headers=headers, json=data)

        self.assertEqual(resp.status_code, 403)
        expected_message = {
            "message": "Advanced users cannot change category_id"
        }
        self.assertEqual(resp.json, expected_message)

    def test_update_others_recipe_difficulty_by_advanced_user(self):
        other_category, recipe, headers = self.create_info()

        data = {
            "difficulty_level": "medium"
        }

        resp = self.client.put(f"/recipe/{recipe.id}", headers=headers, json=data)

        self.assertEqual(resp.status_code, 200)
        expected_message = f"Recipe named '{recipe.recipe_name}' has been updated"
        self.assertEqual(resp.json, expected_message)


class TestDeleteRecipe(APIBaseTestCase):

    def test_recipe_delete_success(self):
        recipe, headers, user = self.create_recipe()

        resp = self.client.delete(f"/{user.username}/recipes/{recipe.id}", headers=headers)

        self.assertEqual(resp.status_code, 200)

        recipes = RecipeModel.query.all()
        self.assertEqual(len(recipes), 0)

        expected_message = f"Recipe named '{recipe.recipe_name}' has been deleted"
        self.assertEqual(resp.json, expected_message)
