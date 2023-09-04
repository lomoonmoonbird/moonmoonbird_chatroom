#--*-- coding:utf-8 --*--

from app.utils.middlewares import handle_exception, handle_log, handle_auth

def init_middlewares(app):
    app.middlewares.append(handle_auth)
    app.middlewares.append(handle_exception)
    app.middlewares.append(handle_log)