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

        return init(self.loop, ['-c', '../config/app.yaml'])

    # the unittest_run_loop decorator can be used in tandem with
    # the AioHTTPTestCase to simplify running
    # tests that are asynchronous
    @unittest_run_loop
    async def test_example(self):
        request = await self.client.request("GET", "/")
        # assert request.status == 200
        text = await request.text()
        print (text)
        # assert "Hello, world" in text

    @unittest_run_loop
    async def test_post_thread(self):
        data = {'title': '是萨达是',
                "content": "发的Dfdfdffdsf ",
                'tags':['python','algorithm','imgs'],
                "imgs": ["a",'b'],
                "category": 1,
                "subtype": 2}
        request = await self.client.request('post', '/api/blog/threads', data=json.dumps(data), headers={"Content-Type":"application/json"})
        text = await request.text()
        print (text)

    @unittest_run_loop
    async def test_get_thread(self):
        request = await self.client.request('get', '/api/blog/threads/1?page_type=1&create_time=1592873621233&thread_type=1', headers={"Content-Type":"application/json"})
        text = await request.text()
        print (text)

    @unittest_run_loop
    async def test_detail_thread(self):
        request = await self.client.request('get', '/api/blog/thread', headers={"Content-Type":"application/json"})
        text = await request.text()
        # print (text)
    @unittest_run_loop
    async def test_test_thread(self):
        request = await self.client.request('get', '/api/blog/test/1', headers={"Content-Type":"application/json"})
        text = await request.text()
        # print (text)