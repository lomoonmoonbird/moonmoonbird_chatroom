#--*-- coding: utf-8 --*--

import pathlib

from app.handlers.api.auth_api import Auth
from app.handlers.ws.room import ChatRoom

PROJECT_ROOT = pathlib.Path(__file__).parent


def init_routers(app):
    prefix = '/api'
    admin = '/admin'

    auth = Auth()
    chatroom = ChatRoom()

    #auth
    app.router.add_post(prefix + '/auth/signup', auth.signup)
    app.router.add_post(prefix + '/auth/signin', auth.signin)

    #room
    app.router.add_get(prefix + '/chat/room', chatroom.room_chat)


    # app.router.add_get('/api/blog/threads', get_threads)
    # app.router.add_get('/api/blog/thread', thread_detail)


    # app.router.add_get('/poll/{question_id}', poll, name='poll')
    # app.router.add_get('/poll/{question_id}/results',
    #                    results, name='results')
    # app.router.add_post('/poll/{question_id}/vote', vote, name='vote')

