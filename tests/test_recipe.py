from db import db
from models import UserRoles, RecipeModel, CategoryModel
from schemas.response.recipe import ResponseRecipeSchema
from tests.base import APIBaseTestCase
from tests.factories import UserFactory


class TestRecipe(APIBaseTestCase):

    def test_recipe_request_schema_missing_fields(self):
        matching_user = UserFactory(username="validuser", role=UserRoles.beginner)
        headers = self.return_authorization_headers(matching_user)

        recipes = RecipeModel.query.all()
        self.assertEqual(len(recipes), 0)

        data = {}

        resp = self.client.post("/validuser/recipes", headers=headers, json=data)

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

        category_name = self.create_category()[0]
        category = (db.session.execute(db.select(CategoryModel)
                                       .filter_by(category_name=category_name)).scalar())

        data = {
            "recipe_name": "L",  # invalid
            "portions": 15,
            "preparing_time_in_minutes": 20,
            "cooking_time_in_minutes": 30,
            "ingredients": "1 (20 ounce) can pineapple rings, ¼ cup water, or as needed, ½ cup unsalted butter, 1 (15.25 ounce) package white cake mix (such as Betty Crocker Super Moist), ½ cup vegetable oil, 3 large egg whites, 1 ½ cups brown sugar, 7 maraschino cherries",
            "description": "Preheat the oven to 350 degrees F (175 degrees C). Drain canned pineapple into a 1-cup measure. Add water if needed to measure 1 cup. Set aside juice and 7 pineapple rings for the cake. Set any remaining juice and rings aside for another use. Melt butter in a 10- or 11-inch cast iron skillet over medium-high heat............",
            "category_id": category.id
        }

        resp = self.client.post("/validuser/recipes", headers=headers, json=data)

        self.assertEqual(resp.status_code, 400)

        expected_message = {"message": "Invalid fields: {'recipe_name': ['Shorter than minimum length 2.']}"}
        self.assertEqual(resp.json, expected_message)

        recipes = RecipeModel.query.all()
        self.assertEqual(len(recipes), 0)

    def test_recipe_create(self):
        recipe_name, headers = self.create_recipe()

        return recipe_name

    def test_recipe_create_with_photo(self):
        pass

    def test_nonexisting_user_with_recipe(self):
        recipe_name, headers = self.create_recipe()
        recipe = (db.session.execute(db.select(RecipeModel)
                                     .filter_by(recipe_name=recipe_name)).scalar())
        recipe_id_unmatched = recipe.id + 1

        updated_data = {
            "recipe_name": "Other Name"
        }

        resp = self.client.put(f"/validuser/recipes/{recipe_id_unmatched}", headers=headers, json=updated_data)

        self.assertEqual(resp.status_code, 404)

        recipes = RecipeModel.query.all()
        self.assertEqual(len(recipes), 1)

        expected_message = {"message": "No user with this recipe"}
        self.assertEqual(resp.json, expected_message)

    def test_recipe_update_success(self):
        recipe_name, headers = self.create_recipe()
        recipe = (db.session.execute(db.select(RecipeModel)
                                     .filter_by(recipe_name=recipe_name)).scalar())

        updated_data = {
            "recipe_name": "Other Name",
            "portions": 4
        }

        resp = self.client.put(f"/validuser/recipes/{recipe.id}", headers=headers, json=updated_data)

        self.assertEqual(resp.status_code, 200)

        recipes = RecipeModel.query.all()
        self.assertEqual(len(recipes), 1)

        sorted_data = dict(sorted(updated_data.items()))
        fields = ", ".join(key for key in sorted_data.keys())

        expected_message = f"The fields {fields} has been updated"
        self.assertEqual(resp.json, expected_message)

    def test_recipe_delete_success(self):
        recipe_name, headers = self.create_recipe()
        recipe = (db.session.execute(db.select(RecipeModel)
                                     .filter_by(recipe_name=recipe_name)).scalar())

        resp = self.client.delete(f"/validuser/recipes/{recipe.id}", headers=headers)

        self.assertEqual(resp.status_code, 200)

        recipes = RecipeModel.query.all()
        self.assertEqual(len(recipes), 0)

        expected_message = f"Recipe named '{recipe_name}' has been deleted"
        self.assertEqual(resp.json, expected_message)

    def test_get_single_recipe(self):
        recipe_name, headers = self.create_recipe()
        recipe = (db.session.execute(db.select(RecipeModel)
                                     .filter_by(recipe_name=recipe_name)).scalar())

        resp = self.client.get(f"/recipe/{recipe.id}", headers=headers)

        self.assertEqual(resp.status_code, 200)

        expected_message = ResponseRecipeSchema().dump(recipe)
        self.assertEqual(resp.json, expected_message)
