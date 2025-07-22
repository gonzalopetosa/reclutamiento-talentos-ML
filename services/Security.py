import jwt
import datetime
import pytz
from dotenv import load_dotenv
import os
from flask import abort

load_dotenv()

class Security():

    secret = os.getenv('JWT_SECRET')
    expiration_time = int(os.getenv('JWT_EXPIRATION'))
    tz = pytz.timezone('America/Argentina/Buenos_Aires')

    @classmethod
    def generate_token(cls, authenticated_user):

        payload = {
            'iat': datetime.datetime.now(tz = cls.tz),
            'exp': datetime.datetime.now(tz = cls.tz) + datetime.timedelta(seconds=cls.expiration_time),
            'email': authenticated_user.email
        }
        return jwt.encode(payload, cls.secret, algorithm='HS256')

    @classmethod
    def validate_token(cls, headers):
        if 'Authorization' in headers.keys():
            authorization = headers['Authorization']

            try:
                encoded_token = authorization.split(" ")[1]
            except IndexError:
                abort(401, 'Malformed Authorization header')

            if len(encoded_token.split('.')) != 3:
                abort(401, "Invalid JWT token: must have 3 segments separated by '.'")

            if (len(encoded_token) > 0):
                try:
                    payload = jwt.decode(encoded_token, cls.secret, algorithms=["HS256"])
                    return True
                except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                    return False
        else:
            return False



