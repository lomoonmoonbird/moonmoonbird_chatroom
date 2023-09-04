import asyncio
import os
import json
import concurrent.futures
import logging
from enum import Enum, unique
from aiojobs.aiohttp import setup,spawn
import aiohttp.web
from functools import partial
from app.utils.decorators import arg_parser
import functools
from app.utils.decorators import arg_parser
from asyncio import Queue
from app.utils.type_enum import ChatCommandType
from app.utils.decorators import authentication
import pickle
from app.utils.exceptions import DuplicateConnError
from app.handlers.ws.chat_base import ChatBase

class MessageType(Enum):
    Enter = 0
    Leave = 1
    BroadCast = 2

class MessageContent(Enum):
    Welcome = "{email} joined the room"
    ByeBye = "{email} leave the room"

class UserSession():
    def __init__(self, user, ws, queue):
        self.ws = ws
        self.user = user
        self.queue = queue

    def __eq__(self, other):
        return self.user == other.user

class ChatRoom(ChatBase):
    def __init__(self):
        super(ChatRoom, self).__init__()
        self.default_room = 0
        self.sem = asyncio.BoundedSemaphore(100)


    @arg_parser(("token", str))
    @authentication()
    async def room_chat(self, request):
        if UserSession(request.requestdata['user'], None, None) in self.connect_users:
            raise DuplicateConnError("you have already connect")
        self.mongo_db = request.app['mongo_db']
        ws = aiohttp.web.WebSocketResponse()

        # #todo 如果未准备 做些什么
        #available = ws.can_prepare(request)
        # if not available:
        #     pass
        await ws.prepare(request)


        chat = request.app.loop.create_task(
                self._enter_room(request.requestdata['user'], ws)
        )
        try:

            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.close:
                    print('websocket connection closed')
                    await self._send_message(request.requestdata['user'],
                                             ws,
                                             MessageType.Leave,
                                             "bye bye %s"%request.requestdata['user']['email'])
                    break
                elif msg.data == aiohttp.WSMsgType.error:
                    print ('ws connection closed with exception %s' % ws.exception())
                    break
                elif msg.type == aiohttp.WSMsgType.text:
                    print ("comming msg", msg.data)
                    # await ws.send_json({'msg': "aaaaaa"})
                    # await self._send_message(request.requestdata['user'], ws, MessageType.BroadCast)
                    await self._send_message(request.requestdata['user'],
                                             ws,
                                             MessageType.BroadCast,
                                             msg.data)
                else:
                    print('ws connection received unknown message type %s' % msg.type)
            #promote user exist
            ret = await spawn(request,self._leave_room(request.requestdata['user'], ws))
            await ws.close()
            chat.cancel()
            return ws
        finally:
            import traceback
            traceback.print_exc()
            print ('close')
            chat.cancel()
            await ws.close()


    async def _chat_loop(self, user_session):
        try:
            while True:
                msg = await user_session.queue.get()
                logging.info("queue message %s" % msg)
                await  user_session.ws.send_json({"msg": msg})
        except concurrent.futures._base.CancelledError:
            import traceback
            traceback.print_exc()
            pass
        finally:
            pass



    async def _send_message(self, user, ws, message_type, msg=''):
        logging.info( "%s send msgtype %s. msg: %s" % (user, message_type.value,msg))
        if message_type == MessageType.Enter:
            for peer in self.connect_users:
                await peer.queue.put(msg)
        elif message_type == MessageType.BroadCast:
            for peer in self.connect_users:
                if UserSession(user, ws, None) != peer:
                    await peer.queue.put(msg)
        elif message_type == MessageType.Leave:
            for peer in self.connect_users:
                await peer.queue.put("xxxxx has left")
        else:
            return None


    async def _enter_room(self, user, ws):
        """
        进入聊天室
        :param user:
        :param ws:
        :return:
        """
        user_session = UserSession(user, ws, Queue())

        self.connect_users.append(user_session) if user_session not in self.connect_users else None


        update_ret = await self.mongo_db[self.chat_database][self.online_user].\
            update_one(filter={"email": user['email']},
                       update={"$set": {"status": "online"}},
                       upsert=True)
        await self._send_message(user, ws, MessageType.Enter,"welcome %s" % user['email'])
        await self._chat_loop(user_session)
        return update_ret

    async def _leave_room(self, user, ws):
        """
        离开聊天室
        :param user:
        :param ws:
        :return:
        """
        self.connect_users.remove(UserSession(user, ws, None))
        await self._send_message(user, ws, MessageType.Leave,"bye bye %s" % user['email'])
        delete_ret = await self.mongo_db[self.chat_database][self.online_user].remove({"email": user['email']})
        return delete_ret

