#--*-- coding: utf-8 --*--

import logging
from aiohttp import web
from app.utils.error_codes import ErrorCodes

class MMBaseApi(object):
    def __init__(self):
        pass


    async def error_404(self):
        return web.json_response(data='',status=404)

    async def reply_ok(self, resp):
        response = {"status": ErrorCodes.Ok.value, "message": "Ok", "data": {"result": resp if resp else []}}
        # logging.info(response)
        return web.json_response(data = response)

    @classmethod
    async def ws_reply_error(cls, request, code, msg, resp=''):
        response = {"status": code.value, "message": msg, "data": {"result": resp if resp else []}}
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        ws.send_json(response)
        await ws.close()
        return ws

    async def reply_ok_with_encoder(self, resp):
        """
            对象转化成可序列化的json.
        :param resp:
        :return:
        """
        json_resp = json.dumps(resp, cls=CJsonEncoder)
        response = {"status": ErrorCodes.Ok.value, "message": "Ok", "data": {"result": json_resp if resp else []}}

        return web.json_response(data=response)

    @classmethod
    async def reply_error(cls, code, msg,value=''):
        response = {"code": code, "errmsg": msg, "data": {"result": value if value else []}}
        # logging.info(response)
        return web.json_response(data = response)