from models.enums import UserRoles, ProfileStatus
from models.user import UserModel
from schemas.response.user import UserInfoResponse
from tests.base import APIBaseTestCase
from tests.factories import UserFactory


class TestUserInfo(APIBaseTestCase):
    def test_get_user_info(self):
        users = UserModel.query.all()
        self.assertEqual(len(users), 0)

        user = UserFactory(role=UserRoles.beginner, profile_status=ProfileStatus.active)
        headers = self.return_authorization_headers(user)

        resp = self.client.get(f"/{user.username}/personal_info", headers=headers)

        users = UserModel.query.all()
        self.assertEqual(len(users), 1)

        self.assertEqual(resp.status_code, 200)
        expected_message = UserInfoResponse().dump(users[0])
        self.assertEqual(resp.json, expected_message)

    def test_update_personal_info(self):
        users = UserModel.query.all()
        self.assertEqual(len(users), 0)

        user = UserFactory()
        headers = self.return_authorization_headers(user)

        data = {
            "phone": "0123456789"
        }

        resp = self.client.put(f"/{user.username}/personal_info", headers=headers, json=data)

        users = UserModel.query.all()
        self.assertEqual(len(users), 1)

        self.assertEqual(resp.status_code, 200)
        expected_message = "Personal info has been updated"
        self.assertEqual(resp.json, expected_message)

        self.assertEqual(users[0].first_name, user.first_name)
        self.assertEqual(users[0].last_name, user.last_name)
        self.assertEqual(users[0].phone, data["phone"])

    def test_phone_field(self):
        users = UserModel.query.all()
        self.assertEqual(len(users), 0)

        user = UserFactory()
        headers = self.return_authorization_headers(user)

        data = {
            "phone": "01234589"
        }

        resp = self.client.put(f"/{user.username}/personal_info", headers=headers, json=data)

        users = UserModel.query.all()
        self.assertEqual(len(users), 1)

        self.assertEqual(resp.status_code, 400)
        expected_message = {
            "message": "Invalid fields: {'phone': ['Shorter than minimum length 10.']}"
        }

        self.assertEqual(resp.json, expected_message)

        self.assertEqual(users[0].first_name, user.first_name)
        self.assertEqual(users[0].last_name, user.last_name)
        self.assertEqual(users[0].phone, user.phone)
