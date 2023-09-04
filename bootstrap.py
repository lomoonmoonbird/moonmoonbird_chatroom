import argparse
import asyncio
import logging
import sys
import os
from aiohttp import web
from aiojobs.aiohttp import setup
from app.init.db import init_mongodb, close_mongodb, init_mysql, close_mysql
from app.init.routers import init_routers
from app.utils.parse_config import TRAFARET
from app.utils.signals import response_header
from app.init.middlewares import init_middlewares
from trafaret_config import commandline


def init(loop, argv):
    ap = argparse.ArgumentParser()
    config_path = os.path.dirname(__file__) + '/app/config/app_dev.yaml'
    commandline.standard_argparse_options(ap,
                                          default_config=config_path)
    #
    # define your command-line arguments here
    #
    options = ap.parse_args(argv)

    config = commandline.config_from_options(options, TRAFARET)

    # setup application and extensions
    app = web.Application(loop=loop)

    # load config from yaml file in current dir
    app['config'] = config

    # create connection to the database
    app.on_startup.append(init_mongodb)
    # shutdown db connection on exit
    app.on_cleanup.append(close_mongodb)
    # create connection to the database
    # app.on_startup.append(init_mysql)
    # shutdown db connection on exit
    # app.on_cleanup.append(close_mysql)
    # setup views and routes
    app.on_response_prepare.append(response_header)
    init_routers(app)
    #middleware
    init_middlewares(app)
    setup(app)
    return app


def main(argv):
    # init logging
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()

    app = init(loop, argv)
    web.run_app(app,
                host=app['config']['host'],
                port=app['config']['port'])
    return app

if __name__ == '__main__':
    print (sys.argv[1:], '@@@@')
    main(sys.argv[1:])