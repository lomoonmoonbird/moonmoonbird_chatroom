#--*-- coding:utf-8 --*--

import json
from aiohttp.web import middleware
from aiohttp import web
from app.utils.exceptions import RequestParamError, JWTokenError, DuplicateConnError
import logging
import aiohttp
from app.handlers.base import MMBaseApi
from app.utils.error_codes import ErrorCodes
from aiohttp.web import WebSocketResponse

@middleware
async def handle_exception(request, handler):
    if request.method == "OPTIONS":
        return web.json_response('')
    try:
        resp = await handler(request)
        logging.info("response correct")
        return resp
    except RequestParamError as rp:
        logging.info(rp.message)
        return web.json_response(rp.message)
    except JWTokenError as jte:
        return await MMBaseApi.ws_reply_error(request, jte.code,jte.message)
    except DuplicateConnError as dce:
        return await MMBaseApi.ws_reply_error(request, dce.code, dce.message)

@middleware
async def handle_log(request, handler):
    print (request.transport.get_extra_info('peername'), '@@@')
    print (request.remote)
    resp = await handler(request)
    return resp


@middleware
async def handle_auth(request, handler):

    if request.path in ['/api/auth/signin', '/api/auth/signup']:
        return await handler(request)
    try:
        pass
        # jwt_token = request.headers['Authorization']
        # jwt.decode(jwt_token, key=request.app['config']['jwt']['salt'].encode('utf-8'),verify=True,algorithms='HS256')
    except KeyError as ke:
        print (ke)
        return WebSocketResponse()
    except jwt.exceptions.DecodeError as de:
        print (de)
        return WebSocketResponse()

    resp = await handler(request)
    return resp

# async def handle_exception(app, handler):
#     print ('app', app)
#     async def handle(request):
#         return await handler(request)
#     return handle




