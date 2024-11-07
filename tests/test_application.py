from unittest.mock import patch

from models import UserRoles, UserModel
from services.sendgrid import SendGridService
from tests.base import APIBaseTestCase
from tests.factories import UserFactory


class TestApp(APIBaseTestCase):

    @staticmethod
    def login_required_endpoints():
        endpoints = (
            ("GET", "/username/personal_info"),
            ("PUT", "/username/personal_info"),
            ("GET", "/username>/personal_photo"),
            ("POST", "/username>/personal_photo"),
            ("DELETE", "/username>/personal_photo"),
            ("PUT", "/username/deactivate_profile"),
            ("PUT", "/username/change-password"),
            ("POST", "/categories"),
            ("PUT", "/category/1"),
            ("DELETE", "/category/1"),
            ("GET", "/username/recipes"),
            ("POST", "/username/recipes"),
            ("PUT", "/username/recipes/1"),
            ("DELETE", "/username/recipes/1"),
            ("POST", "/username/recipes/1/photos"),
            ("DELETE", "/username/recipes/1/photos/1"),
            ("PUT", "/recipe/1"),
            ("POST", "/recipe/1/comment"),
            ("PUT", "/recipe/1/comment/1"),
            ("DELETE", "/recipe/1/comment/1")
        )

        return endpoints

    def test_login_required_endpoints_missing_token(self):

        endpoints = self.login_required_endpoints()

        for method, url in endpoints:
            resp = self.make_request(method, url)

            self.assertEqual(resp.status_code, 401)
            expected_message = {"message": "Invalid or missing token"}
            self.assertEqual(resp.json, expected_message)

    def test_login_required_endpoints_invalid_token(self):

        endpoints = self.login_required_endpoints()
        headers = {
            "Authorization": "Bearer invalid"
        }

        for method, url in endpoints:
            resp = self.make_request(method, url, headers=headers)

            self.assertEqual(resp.status_code, 401)
            expected_message = {"message": "Invalid or missing token"}
            self.assertEqual(resp.json, expected_message)

    @staticmethod
    def validate_logged_user_endpoints():
        endpoints = (
            ("GET", "/validuser/personal_info"),
            ("PUT", "/validuser/personal_info"),
            ("GET", "/validuser/personal_photo"),
            ("POST", "/validuser/personal_photo"),
            ("DELETE", "/validuser/personal_photo"),
            ("PUT", "/validuser/deactivate_profile"),
            ("PUT", "/validuser/change-password"),
            ("POST", "/validuser/recipes"),
            ("PUT", "/validuser/recipes/1"),
            ("DELETE", "/validuser/recipes/1"),
            ("POST", "/validuser/recipes/1/photos"),
            ("DELETE", "/validuser/recipes/1/photos/1"),
        )

        return endpoints

    def test_validate_logged_user_nonmatching_username(self):
        endpoints = self.validate_logged_user_endpoints()

        nonmatching_user = UserFactory(username="differentuser")
        headers = self.return_authorization_headers(nonmatching_user)

        for method, endpoint in endpoints:
            resp = self.make_request(method, endpoint, headers=headers)
            self.assertEqual(resp.status_code, 404)
            expected_message = {"message": "User not found"}
            self.assertEqual(resp.json, expected_message)

    def permission_required(self, endpoints, headers):

        for method, url in endpoints:
            resp = self.make_request(method, url, headers=headers)

            self.assertEqual(resp.status_code, 403)
            expected_message = {
                "message": "You do not have permissions to access this resource"
            }
            self.assertEqual(resp.json, expected_message)

    @staticmethod
    def category_permission_required_endpoints():
        endpoints = (
            ("POST", "/categories"),
            ("PUT", "/category/1"),
            ("DELETE", "/category/1")
        )

        return endpoints

    def test_permission_required_categories_endpoints_beginner_user(self):
        endpoints = self.category_permission_required_endpoints()

        user = UserFactory()
        headers = self.return_authorization_headers(user)

        self.permission_required(endpoints, headers)

    def test_permission_required_categories_endpoints_advanced_user(self):
        endpoints = self.category_permission_required_endpoints()

        user = UserFactory(role=UserRoles.advanced)
        headers = self.return_authorization_headers(user)

        self.permission_required(endpoints, headers)

    def test_permission_required_create_recipe_admin(self):
        endpoints = (
            ("POST", "/validuser/recipes"),
        )

        matching_user = UserFactory(username="validuser", role=UserRoles.admin)
        headers = self.return_authorization_headers(matching_user)

        resp = self.client.post("/validuser/recipes", headers=headers)
        self.assertNotEqual(resp.status_code, 404)

        self.permission_required(endpoints, headers)


class TestRegisterSchema(APIBaseTestCase):

    def test_register_schema_missing_fields(self):

        users = UserModel.query.all()
        self.assertEqual(len(users), 0)

        required_fields = ["email", "password", "username"]

        data = {}

        resp = self.client.post("/register", json=data)
        self.assertEqual(resp.status_code, 400)
        error_message = resp.json["message"]
        for field in required_fields:
            self.assertIn(field, error_message)

        users = UserModel.query.all()
        self.assertEqual(len(users), 0)

        data = {
            "email": "hello@hello.com",
            "password": "Hello123!",
            "username": "hello",
        }

        required_fields = ["first_name", "last_name"]

        resp = self.client.post("/register", json=data)
        self.assertEqual(resp.status_code, 400)
        error_message = resp.json["message"]
        for field in required_fields:
            self.assertIn(field, error_message)

    def test_register_schema_invalid_username_field(self):
        data = {
            "email": "hello@hello.com",
            "password": "Hello123!",
            "username": "hello asgfs",
            "first_name": "hey",
            "last_name": "hay"
        }

        resp = self.client.post("/register", json=data)
        self.assertEqual(resp.status_code, 400)
        error_message = resp.json["message"]
        expected_message = "Invalid fields: {'username': ['Username cannot contain spaces. Must be one word!']}"
        self.assertEqual(error_message, expected_message)

    @patch.object(SendGridService, "send_email")
    def test_register(self, mock_sendgrid):
        self.register_user()


class TestLoginSchema(APIBaseTestCase):

    def test_login(self):
        email, password, user = self.register_user()

        login_data = {
            "email": email,
            "password": password
        }

        resp = self.client.post("/login", json=login_data)
        self.assertEqual(resp.status_code, 200)
        token = resp.json["token"]
        self.assertIsNotNone(token)

    def test_login_invalid_email(self):
        email, password, user = self.register_user()

        login_data = {
            "email": "invalid@invalid.com",
            "password": password
        }

        self.assertNotEqual(email, login_data["email"])

        user = UserModel.query.filter_by(email=login_data["email"]).all()
        self.assertEqual(len(user), 0)

        resp = self.client.post("/login", json=login_data)
        self.assertEqual(resp.status_code, 401)
        message = resp.json
        expected_message = {
            "message": "Invalid email or password. Please try again."
        }
        self.assertEqual(message, expected_message)

    def test_login_invalid_password(self):
        email, password, user = self.register_user()

        login_data = {
            "email": email,
            "password": "password"
        }

        self.assertNotEqual(password, login_data["password"])

        user = UserModel.query.filter_by(email=email).all()
        self.assertEqual(len(user), 1)

        resp = self.client.post("/login", json=login_data)
        self.assertEqual(resp.status_code, 401)
        message = resp.json
        expected_message = {
            "message": "Invalid email or password. Please try again."
        }
        self.assertEqual(message, expected_message)
