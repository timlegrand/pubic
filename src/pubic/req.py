import random
import asyncio
from aiohttp import ClientSession


async def fetch(session, endpoint, access_token, container_name="default", object_path=""):
    headers = { "X-Auth-Token": f"{access_token}" }
    url = endpoint + "/" + container_name + "/" + object_path
    async with session.head(url, headers=headers) as response:
        # print("{}".format(response.url))
        return response.headers, object_path


async def bound_fetch(sem, session, endpoint, access_token, container_name="default", object_path=""):
    async with sem:
        return await fetch(session, endpoint, access_token, container_name, object_path)


async def get_all(objects, endpoint, access_token, container_name="default"):
    tasks = []
    results = []
    # Limit simultaneous connections
    sem = asyncio.Semaphore(1000)

    async with ClientSession() as session:
        for o in objects:
            task = asyncio.create_task(bound_fetch(sem, session, endpoint, access_token, container_name, o))
            tasks.append(task)

        for t in tasks:
            results.append(await t)
        # print(results)
        return results


def run_all(objects, endpoint, access_token, container_name="default"):
    objects_properties = []
    objects_properties = asyncio.run(get_all(objects, endpoint, access_token, container_name))
    return objects_properties
