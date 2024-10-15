from werkzeug.exceptions import BadRequest, Unauthorized, Forbidden, NotFound
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from managers.auth import AuthManager, auth
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

    @staticmethod
    def login(user_data):

        user = db.session.execute(db.select(UserModel).filter_by(email=user_data["email"])).scalar()

        if user:
            password_is_valid = check_password_hash(user.password, user_data["password"])

        if not user or not password_is_valid:
            raise Unauthorized ("Invalid username or password. Please try again.")

        return AuthManager.encode_token(user)

    @staticmethod
    def change_password(username, password_data):
        current_user = auth.current_user()

        if username != current_user.username:
            raise Forbidden("You don not have permissions to access this resource")

        validate_password = check_password_hash(current_user.password, password_data["old_password"])

        if not validate_password:
            raise NotFound("Wrong or invalid password! Please try again!")

        new_password_hash = generate_password_hash(password_data["new_password"], method='pbkdf2:sha256')

        db.session.execute(
            db.update(UserModel)
            .where(UserModel.id == current_user.id)
            .values(password=new_password_hash)
        )
