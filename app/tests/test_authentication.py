from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aiohttp import web
from bootstrap import init
import sys
import json
from app.init.routers import init_routers
from app.init.db import init_mongodb

class MyAppTestCase(AioHTTPTestCase):
    async def get_application(self):
        """
        Override the get_app method to return your application.
        """

        return init(self.loop, ['-c', '../config/app_dev.yaml'])

    @unittest_run_loop
    async def test_signup(self):
        data = {'email': 'lomoonmoonbird2@gmail.com',"password": "moonmoonbird"}
        request = await self.client.request('post', '/api/auth/signup', data=json.dumps(data), headers={"Content-Type":"application/json"})
        text = await request.text()
        print (text)


    @unittest_run_loop
    async def test_signin(self):
        data = {'email': 'lomoonmoonbird@gmail.com',"password": "moonmoonbird"}
        print ('==')
        request = await self.client.request('post', '/api/auth/signin', data=json.dumps(data), headers={"Content-Type":"application/json"})
        text = await request.text()
        print (text)