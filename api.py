import sys
import os
import time
import json
import logging

import aiopg
import aioredis
from aiohttp import web

logger = logging.getLogger('api')
logger.setLevel(logging.DEBUG)
stdout_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(name)s[%(process)d] - %(pathname)s:%(lineno)d :: %(message)s'
)
stdout_handler.setFormatter(formatter)
stdout_handler.setLevel(logging.DEBUG)
logger.addHandler(stdout_handler)


REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = os.environ['REDIS_PORT']
REDIS_QUEUE = os.environ['REDIS_QUEUE']


routes = web.RouteTableDef()


@web.middleware
async def logging_middleware(request, handler):
    logger.info('New request to %s. Payload: %s', request.path, await request.text())
    return await handler(request)


@routes.post('/schedule')
async def healthcheck(request: web.Request):
    request_data = await request.json()
    item_id = request_data['item_id']

    query = f"INSERT INTO items (item_id) values ('{item_id}');"
    async with request.app['postgres'].acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query)

    job_data = json.dumps({'item_id': request_data['item_id']})
    request.app['redis'].lpush(REDIS_QUEUE, job_data)
    return web.json_response({'msg': 'ok'})


async def create_app():
    app = web.Application(middlewares=[
        logging_middleware
    ])
    app['redis'] = await aioredis.create_redis_pool(
        f'redis://{REDIS_HOST}:{REDIS_PORT}',
        maxsize=20
    )
    app['postgres'] = await aiopg.create_pool(
        'postgres://postgres:postgres@arteia-database:5432/arteia_db'
    )

    app.add_routes(routes)

    return app


if __name__ == '__main__':
    time.sleep(5)  # naive wait for redis & postgres
    web.run_app(create_app(), port=5000)
