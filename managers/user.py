from werkzeug.exceptions import BadRequest, Unauthorized, NotFound
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from managers.auth import AuthManager, auth
from managers.photo import PhotoManager
from models import UserModel, ProfileStatus
from services.sendgrid import SendGridService

sendgrid = SendGridService()


class UserManager:

    @staticmethod
    def register(user_data):

        user_data['password'] = generate_password_hash(user_data['password'], method='pbkdf2:sha256')
        user = UserModel(**user_data)

        try:
            db.session.add(user)
            db.session.flush()

            sendgrid.send_email(
                recipient=["ilearntosendmails@mail.bg"],  # here it can be a user's email (user.email)
                subject=f"Welcome to our delicious country {user.first_name} {user.last_name}",
                content=f"Hello {user.username},\n "
                        f"We expect your delicious recipes to reach a wide range of people.\n"
                        f"Best Regards,\n"
                        f"Delicious Recipe"
            )

            return AuthManager.encode_token(user)
        except Exception as ex:
            raise BadRequest(str(ex))

    @staticmethod
    def login(user_data):

        user = db.session.execute(db.select(UserModel).filter_by(email=user_data["email"])).scalar()

        if user:
            password_is_valid = check_password_hash(user.password, user_data["password"])

        if not user or not password_is_valid:
            raise Unauthorized("Invalid email or password. Please try again.")

        return AuthManager.encode_token(user)

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
    def add_user_photo(username, data):
        user_id = UserManager.get_user(username).id
        existing_photo = PhotoManager().get_photo(user_id, "user").first()

        if existing_photo:
            raise BadRequest("You cannot add another profile picture")

        photo_url = PhotoManager().create_photo_url(data["photo"], data["photo_extension"], "user")
        photo_model = PhotoManager().create_photo(photo_url, user_id, "user")

        return photo_model

    @staticmethod
    def update_user_info(username, data):

        for key, value in data.items():
            db.session.execute(
                db.update(UserModel)
                .where(UserModel.username == username)
                .values(**{key: value})
            )

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
    def deactivate_profile(username):
        user = UserManager.get_user(username)

        db.session.execute(
            db.update(UserModel)
            .where(UserModel.username == username)
            .values(profile_status=ProfileStatus.inactive)
        )

        return user
