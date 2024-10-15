from datetime import datetime, timedelta, timezone

import jwt
from decouple import config
from flask_httpauth import HTTPTokenAuth
from werkzeug.exceptions import Unauthorized, NotFound, Forbidden
from werkzeug.security import check_password_hash, generate_password_hash

from db import db
from models import UserModel


class AuthManager:
    @staticmethod
    def encode_token(user):
        try:
            payload = {
                'exp': datetime.now(timezone.utc) + timedelta(days=2),
                'sub': user.id
            }
            return jwt.encode(
                payload,
                key=config('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            raise e


    @staticmethod
    def decode_token(token):
        try:
            info = jwt.decode(
                jwt=token,
                key=config('SECRET_KEY'),
                algorithms=["HS256"]
            )
            return info['sub']  # user_id

        except Exception as ex:
            raise ex


auth = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def verify_token(token):
    try:
        user_id = AuthManager.decode_token(token)
        return db.session.execute(db.select(UserModel).filter_by(id=user_id)).scalar()
    except Exception as ex:
        raise Unauthorized("Invalid or missing token")
