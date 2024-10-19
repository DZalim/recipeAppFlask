from werkzeug.exceptions import BadRequest, Unauthorized, NotFound
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from managers.auth import AuthManager, auth
from models import UserModel, ProfileStatus


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
            return AuthManager.encode_token(
                user)  # create a token in managers/auth.py and return it in resources/auth.py
        except Exception as ex:
            raise BadRequest(str(ex))

    @staticmethod
    def login(user_data):

        user = db.session.execute(db.select(UserModel).filter_by(email=user_data["email"])).scalar()

        if user:
            password_is_valid = check_password_hash(user.password, user_data["password"])

        if not user or not password_is_valid:
            raise Unauthorized("Invalid username or password. Please try again.")

        return AuthManager.encode_token(user)

    @staticmethod
    def change_password(password_data):
        current_user = auth.current_user()

        validate_password = check_password_hash(current_user.password, password_data["old_password"])

        if not validate_password:
            raise NotFound("Wrong or invalid password! Please try again!")

        new_password_hash = generate_password_hash(password_data["new_password"], method='pbkdf2:sha256')

        db.session.execute(
            db.update(UserModel)
            .where(UserModel.id == current_user.id)
            .values(password=new_password_hash)
        )

    @staticmethod
    def get_user(username):
        user = db.session.execute(db.select(UserModel).filter_by(username=username)).scalar()

        if not user:
            raise NotFound("User not found!")

        return user

    @staticmethod
    def get_personal_info(username):
        return UserManager.get_user(username)

    @staticmethod
    def update_user_info(username, data):

        for key, value in data.items():
            db.session.execute(
                db.update(UserModel)
                .where(UserModel.username == username)
                .values(**{key: value})
            )

    @staticmethod
    def deactivate_profile(username):
        user = UserManager.get_user(username)

        db.session.execute(
            db.update(UserModel)
            .where(UserModel.username == username)
            .values(profile_status=ProfileStatus.inactive)
        )

        return user
