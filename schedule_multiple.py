import uuid
import asyncio
import argparse

import aiohttp


async def make_request():
    url = 'http://localhost:5000/schedule'
    item_id = uuid.uuid4().hex
    payload = {'item_id': item_id}
    async with aiohttp.request('POST', url, json=payload) as response:
        print(f'Response for {item_id}: {response}')


async def make_multiple(num_requests):
    request_coroutines = [make_request() for _ in range(num_requests)]
    await asyncio.gather(*request_coroutines)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--num-requests', type=int, dest='num_requests', default=20)
    args = parser.parse_args()
    asyncio.run(make_multiple(args.num_requests))
