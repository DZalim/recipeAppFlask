from db import db
from models import UserRoles, CategoryModel
from schemas.response.category import CategoryResponseSchema
from schemas.response.recipe import ResponseRecipeSchema
from tests.base import APIBaseTestCase
from tests.factories import UserFactory, CategoryFactory, RecipeFactory


class TestCategory(APIBaseTestCase):

    def test_category_schema_missing_fields(self):
        user = UserFactory(role=UserRoles.admin)
        headers = self.return_authorization_headers(user)

        data = {}

        categories = CategoryModel.query.all()
        self.assertEqual(len(categories), 0)

        resp = self.client.post("/categories", headers=headers, json=data)

        self.assertEqual(resp.status_code, 400)

        expected_message = {
            "message": "Invalid fields: {'category_name': ['Missing data for required field.']}"
        }
        self.assertEqual(resp.json, expected_message)

        categories = CategoryModel.query.all()
        self.assertEqual(len(categories), 0)

    def test_category_schema_invalid_fields(self):
        user = UserFactory(role=UserRoles.admin)
        headers = self.return_authorization_headers(user)

        data = {"category_name": "а"}

        categories = CategoryModel.query.all()
        self.assertEqual(len(categories), 0)

        resp = self.client.post("/categories", headers=headers, json=data)

        self.assertEqual(resp.status_code, 400)

        expected_message = {
            "message": "Invalid fields: {'category_name': ['Shorter than minimum length 2.']}"
        }
        self.assertEqual(resp.json, expected_message)

        categories = CategoryModel.query.all()
        self.assertEqual(len(categories), 0)

    def test_category_create(self):
        category_name, headers = self.create_category()

        return category_name

    def test_category_schema_same_name(self):
        category_name, first_header = self.create_category()

        categories = CategoryModel.query.all()
        self.assertEqual(len(categories), 1)

        user = UserFactory(role=UserRoles.admin)
        headers = self.return_authorization_headers(user)

        data = {
            "category_name": category_name
        }

        resp = self.client.post("/categories", headers=headers, json=data)

        self.assertEqual(resp.status_code, 400)

        expected_message = {
            "message": "Invalid fields: {'category_name': ['Тhis category already exists!']}"
        }
        self.assertEqual(resp.json, expected_message)

        categories = CategoryModel.query.all()
        self.assertEqual(len(categories), 1)

    def test_nonexisting_category(self):
        category_name, headers = self.create_category()
        category = (db.session.execute(db.select(CategoryModel)
                                       .filter_by(category_name=category_name)).scalar())
        category_id_unmatched = category.id + 1

        updated_data = {
            "category_name": "Other Name"
        }

        resp = self.client.put(f"/category/{category_id_unmatched}", headers=headers, json=updated_data)

        self.assertEqual(resp.status_code, 404)

        categories = CategoryModel.query.all()
        self.assertEqual(len(categories), 1)

        expected_message = {"message": "Category Not Found"}
        self.assertEqual(resp.json, expected_message)

    def test_category_update_success(self):
        category_name, headers = self.create_category()
        category = (db.session.execute(db.select(CategoryModel)
                                       .filter_by(category_name=category_name)).scalar())
        category_id = category.id

        updated_data = {
            "category_name": "Updated name"
        }

        resp = self.client.put(f"/category/{category_id}", headers=headers, json=updated_data)

        self.assertEqual(resp.status_code, 200)

        categories = CategoryModel.query.all()
        self.assertEqual(len(categories), 1)

        new_name = updated_data["category_name"]
        expected_message = f"Category with id {category_id} has been updated. Category name is now: {new_name}"
        self.assertEqual(resp.json, expected_message)

    def test_category_delete_success(self):
        category_name, headers = self.create_category()
        category = (db.session.execute(db.select(CategoryModel)
                                       .filter_by(category_name=category_name)).scalar())
        category_id = category.id

        resp = self.client.delete(f"/category/{category_id}", headers=headers)

        self.assertEqual(resp.status_code, 200)

        categories = CategoryModel.query.all()
        self.assertEqual(len(categories), 0)

        expected_message = f"Category named '{category_name}' has been deleted"
        self.assertEqual(resp.json, expected_message)

    def test_get_category(self):
        categories = []

        for i in range(5):
            category = CategoryFactory()
            categories.append(category)

        resp = self.client.get("/categories")

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, CategoryResponseSchema(many=True).dump(categories))

    def test_get_categories_recipes(self):  # TODO: fix this!!! single works, but ...
        category_name = self.create_category()[0]
        category = (db.session.execute(db.select(CategoryModel)
                                       .filter_by(category_name=category_name)).scalar())

        recipes = []
        for i in range(5):
            recipe = RecipeFactory(category_id=category.id, user_id=0)

            recipes.append(recipe)

        resp = self.client.get(f"/categories/{category.id}/recipes")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, ResponseRecipeSchema().dump(recipes, many=True))
