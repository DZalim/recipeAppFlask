from werkzeug.exceptions import BadRequest
from werkzeug.security import generate_password_hash

from db import db
from managers.auth import AuthManager
from models import UserModel


class UserManager:
    @staticmethod
    def register(user_data):
        # hash the submitted registration password
        user_data['password'] = generate_password_hash(user_data['password'], method='pbkdf2:sha256')

        # instantiate a user model
        user = UserModel(**user_data)

        try:
            db.session.add(user)
            db.session.flush()  # waits to check if all data is ok to save to multiple tables, if needed
            return AuthManager.encode_token(user)  # create a token in managers/auth.py and return it in resources/auth.py
        except Exception as ex:
            raise BadRequest(str(ex))
