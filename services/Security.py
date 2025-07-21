import jwt
import datetime
import pytz
from dotenv import load_dotenv
import os

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



