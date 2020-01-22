import asyncio
from aiohttp import ClientSession


async def stat_object(
    session,
    endpoint,
    access_token,
    container_name="default",
    object_path=""):

    headers = { "X-Auth-Token": f"{access_token}" }
    url = endpoint + "/" + container_name + "/" + object_path
    async with session.head(url, headers=headers) as response:
        return response.headers, object_path


async def stat_objects(
    objects,
    endpoint,
    access_token,
    container_name="default"):

    tasks = []
    results = []
    async with ClientSession() as session:
        # Limit simultaneous connections to 1000
        async with asyncio.Semaphore(1000) as sem:
            for path in objects:
                task = asyncio.create_task(stat_object(
                    session,
                    endpoint,
                    access_token,
                    container_name,
                    path))
                tasks.append(task)

            for t in tasks:
                results.append(await t)
            return results


def run_async(function, *args, **kwargs):
    return asyncio.run(function(*args, **kwargs))
