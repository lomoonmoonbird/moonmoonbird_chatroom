#--*-- coding: utf-8 --*--

"""
handler for user signin signout signup
"""

from app.handlers.base import MMBaseApi
from app.utils.decorators import arg_parser
from app.utils.authentication import Authentication

class Auth(MMBaseApi):
    def __init__(self):
        pass

    @arg_parser(("email", str), ("password", str))
    async def signup(self, request):
        print ('@@###')
        auth = Authentication(request.app['config'])

        await auth.signup(request.requestdata['email'],request.requestdata['password'])
        return await self.reply_ok([])


    @arg_parser(("email", str), ("password", str))
    async def signin(self, request):
        auth = Authentication(request.app['config'])
        user = await auth.signin(request.requestdata['email'], request.requestdata['password'])
        return await self.reply_ok(user)