from models.category import CategoryModel
from models.enums import UserRoles
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
        self.create_category()

    def test_category_schema_same_name(self):
        category, category_user_header = self.create_category()

        data = {
            "category_name": category.category_name
        }

        resp = self.client.post("/categories", headers=category_user_header, json=data)

        self.assertEqual(resp.status_code, 400)

        expected_message = {
            "message": "Invalid fields: {'category_name': ['Тhis category already exists!']}"
        }
        self.assertEqual(resp.json, expected_message)

        categories = CategoryModel.query.all()
        self.assertEqual(len(categories), 1)

    def test_nonexisting_category(self):
        category, category_user_header = self.create_category()

        updated_data = {
            "category_name": "Other Name"
        }

        endpoints = (
            ("PUT", f"/category/{category.id + 1}"),
            ("DELETE", f"/category/{category.id + 1}")
        )

        for method, url in endpoints:
            resp = self.make_request(method, url, headers=category_user_header, data=updated_data)

            self.assertEqual(resp.status_code, 404)

            categories = CategoryModel.query.all()
            self.assertEqual(len(categories), 1)

            expected_message = {"message": "Category Not Found"}
            self.assertEqual(resp.json, expected_message)

    def test_category_update_success(self):
        category, category_user_header = self.create_category()

        updated_data = {
            "category_name": "Updated name"
        }

        resp = self.client.put(f"/category/{category.id}", headers=category_user_header, json=updated_data)

        self.assertEqual(resp.status_code, 200)

        categories = CategoryModel.query.all()
        self.assertEqual(len(categories), 1)

        new_name = updated_data["category_name"]
        expected_message = f"Category with id {category.id} has been updated. Category name is now: {new_name}"
        self.assertEqual(resp.json, expected_message)

    def test_category_delete_success(self):
        category, category_user_header = self.create_category()

        resp = self.client.delete(f"/category/{category.id}", headers=category_user_header)

        self.assertEqual(resp.status_code, 200)

        categories = CategoryModel.query.all()
        self.assertEqual(len(categories), 0)

        expected_message = f"Category named '{category.category_name}' has been deleted"
        self.assertEqual(resp.json, expected_message)

    def test_get_category(self):
        categories = []

        for i in range(5):
            category = CategoryFactory()
            categories.append(category)

        resp = self.client.get("/categories")

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, CategoryResponseSchema(many=True).dump(categories))

    def test_get_categories_recipes(self):
        category = self.create_category()[0]

        recipes = []
        for i in range(5):
            user = UserFactory()
            recipe = RecipeFactory(category_id=category.id, user_id=user.id)

            recipes.append(recipe)

        resp = self.client.get(f"/categories/{category.id}/recipes")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, ResponseRecipeSchema().dump(recipes, many=True))
