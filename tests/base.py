from flask_testing import TestCase

from config import create_app
from db import db
from managers.auth import AuthManager
from models import UserModel


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