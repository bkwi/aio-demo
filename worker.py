import os
import sys
import json
import time
import random
import logging

from redis import Redis
from sqlalchemy import create_engine


logger = logging.getLogger('worker')
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

r = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
engine = create_engine('postgres://postgres:postgres@arteia-database:5432/arteia_db')


def cpu_heavy_task(n):
    if n <= 1:
        return n
    return cpu_heavy_task(n-1) + cpu_heavy_task(n-2)


def run():
    logger.info('Worker starting')
    while True:
        queue_name, item = r.brpop(REDIS_QUEUE)

        n = random.randint(25, 35)
        item_id = json.loads(item)['item_id']
        logger.info('Worker received item: %s. Random int: %s', item, n)
        t0 = time.time()
        result = cpu_heavy_task(n)
        logger.info('Result: %s. Time used: %s', result, time.time() - t0)

        query = f"""
            UPDATE items
            SET random_int = {n}, result = {result}
            WHERE item_id = '{item_id}';
        """
        with engine.connect() as conn:
            conn.execute(query)


if __name__ == '__main__':
    time.sleep(5)  # naive wait for redis & postgres
    run()
