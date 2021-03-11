import os
import json
import time
import random

from redis import Redis
from sqlalchemy import create_engine

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
    print('Worker starting')
    while True:
        queue_name, item = r.brpop(REDIS_QUEUE)

        n = random.randint(25, 35)
        item_id = json.loads(item)['item_id']
        print(f'Worker received item: {item}. Random int: {n}')
        t0 = time.time()
        result = cpu_heavy_task(n)
        print(f'Result: {result}. Time used: {time.time() - t0}')

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
