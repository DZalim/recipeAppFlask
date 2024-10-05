from datetime import datetime, timedelta

import jwt
from decouple import config


class AuthManager:
    @staticmethod
    def encode_token(user):
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=2),
                'sub': user.id
            }
            return jwt.encode(
                payload,
                key=config('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            raise e
