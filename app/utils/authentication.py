#--*-- coding: utf-8 --*--

"""
login in service for authenticate user
scheme:
{
    "email": "",
    "username": "",
    "nickname": "",
    "salt": "",
    "password": "",
    "sha256-base64-pwd": "",
    "domain": ["admin", "blog"],
    "role": [].
    "create_time": ,
    "login_time":
}
"""

import time
import hashlib
import hmac
import base64
import jwt
from app.utils.exceptions import UserPasswordNotMatchError, UserNotExistError,\
    UserEmailEmptyError, UserPwdEmptyError, UserExistError

class Authentication:
    def __init__(self, config={}):
        self.config = config
        self.user = {
            "email": "",
            "username": "",
            "nickname": "",
            # "salt": "",
            # "password": "",
            # "sha256-base64-pwd": "",
            "domain": ["admin", "blog"],
            "role": [],
            "create_time": time.time(),
            "login_time": time.time()
        }

    async def signin(self, email='', password='',):
        """
        login with email and password
        :param email
        :param password
        :param app config
        :return:
        """

        self.verify_email_password(email, password)

        user = await self.config['mongo_db'].moonmoonbird.user.find_one({"email": email})
        if not user:
            msg = 'user {} not exist' % email
            raise UserNotExistError(msg)
        raw_password = password.encode('utf-8')
        secret = user['salt']

        sha256_base64_password = base64.b64encode(hmac.new(secret, raw_password, digestmod=hashlib.sha256).digest())
        if sha256_base64_password != user['sha256_base64_pwd'].strip():
            msg = "password not correct"
            raise UserPasswordNotMatchError(msg)

        payload = {
            "email": user['email'],
            "nickname": user['nickname'],
            "exp": int(time.time()) + self.config['jwt']['expire']
        }
        jwt_token = jwt.encode(payload, self.config['jwt']['salt'], algorithm='HS256')
        self.user['jwtoken'] = jwt_token.decode('utf-8')
        return self.user


    def verify_email_password(self, email, password):
        if not email:
            msg = 'email should not be empty' % email
            raise UserEmailEmptyError(msg)
        if not password:
            msg = 'password should not be empty'
            raise UserPwdEmptyError(msg)

    async def signup(self, email, password):
        print ('----')
        self.verify_email_password(email, password)
        user = await self.config['mongo_db'].moonmoonbird.user.find_one({"email": email})
        if user:
            msg = "user %s already exist" % (email,)
            raise UserExistError(msg)

        raw_password = password.encode('utf-8')
        secret = self.generate_salt()
        print (secret)
        sha256_base64_password = base64.b64encode(hmac.new(secret, raw_password, digestmod=hashlib.sha256).digest())
        print (sha256_base64_password)
        user_data = {
            "email": email,
            "username": "",
            "nickname": "",
            "salt": secret,
            "password": password,
            "sha256_base64_pwd": sha256_base64_password,
            "domain": [],
            "role": [],
            "create_time": time.time(),
            "login_time": time.time()
        }
        user_id = await self.config['mongo_db'].moonmoonbird.user.update({"email": email}, user_data, upsert=True)
        print (user_id, '####')
        return

    async def signout(self):
        pass

    def generate_salt(self):
        import secrets
        salt = secrets.token_bytes(16)
        return salt




