from flask_testing import TestCase

from config import create_app
from db import db
from managers.auth import AuthManager
from models import UserModel, UserRoles, CategoryModel, RecipeModel
from tests.factories import UserFactory


def generate_token(user):
    return AuthManager.encode_token(user)


class APIBaseTestCase(TestCase):
    def create_app(self):
        return create_app("config.TestingConfig")

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def register_user(self):
        data = {
            "email": "hello@hello.com",
            "password": "Hello123!",
            "username": "hello",
            "first_name": "hey",
            "last_name": "hay"
        }

        users = UserModel.query.all()
        self.assertEqual(len(users), 0)

        resp = self.client.post("/register", json=data)
        self.assertEqual(resp.status_code, 201)

        token = resp.json["token"]
        self.assertIsNotNone(token)

        return data["email"], data["password"]

    def return_authorization_headers(self, user):
        user_token = generate_token(user)

        headers = {
            "Authorization": f"Bearer {user_token}"
        }

        return headers

    def create_category(self):
        user = UserFactory(role=UserRoles.admin)
        headers = self.return_authorization_headers(user)

        categories = CategoryModel.query.all()
        self.assertEqual(len(categories), 0)

        category_data = {
            "category_name": "Category Name"
        }
        resp = self.client.post("/categories", headers=headers, json=category_data)

        self.assertEqual(resp.status_code, 201)

        categories = CategoryModel.query.all()
        self.assertEqual(len(categories), 1)

        category_name = category_data["category_name"]
        expected_message = f"A category named '{category_name}' has been created"
        self.assertEqual(resp.json, expected_message)

        return category_name, headers

    def create_recipe(self):
        matching_user = UserFactory(username="validuser", role=UserRoles.beginner)
        headers = self.return_authorization_headers(matching_user)

        recipes = RecipeModel.query.all()
        self.assertEqual(len(recipes), 0)

        category_name = self.create_category()[0]
        category = (db.session.execute(db.select(CategoryModel)
                                       .filter_by(category_name=category_name)).scalar())

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
            "category_id": category.id
        }

        resp = self.client.post("/validuser/recipes", headers=headers, json=data)

        self.assertEqual(resp.status_code, 201)

        recipes = RecipeModel.query.all()
        self.assertEqual(len(recipes), 1)

        recipe_name = data["recipe_name"]
        expected_message = f"A recipe named '{recipe_name}' has been created"
        self.assertEqual(resp.json, expected_message)

        return recipe_name, headers
