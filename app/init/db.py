#--*-- coding: utf-8 --*--

import aiomysql
import motor.motor_asyncio

async def init_mysql(app):
    conf = app['config']['mysql']
    pool = await aiomysql.create_pool(host=conf['host'],
                                      port=conf['port'],
                                      user=conf['user'],
                                      password=conf['password'],
                                      db=conf['database'],
                                      loop=app.loop)
    app['mysql_db'] = pool

async def close_mysql(app):
    app['mysql_db'].close()
    await app['mysql_db'].wait_closed()


async def init_mongodb(app):
    conf = app['config']['mongodb']
    pool = motor.motor_asyncio.AsyncIOMotorClient(conf['host'],
                                                  conf['port'],
                                                  maxPoolSize=conf['max_pool_size'])
    app['config']['mongo_db'] = pool
    app['mongo_db'] = pool

async def close_mongodb(app):
    app['config']['mongo_db'].close()
    app['mongo_db'].close()


