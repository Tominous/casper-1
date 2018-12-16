import aiohttp


async def json_get(url, headers=None):
    """
    Asynchronous method to fetch API results as json.
    :param url: The url to make a POST request to.
    :param headers: Optional headers if additional info needs to be passed along
    :return: The json results or None if error
    """
    if headers is None:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    return None
    else:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    return None


async def json_post(url, headers=None):
    """
    Asynchronous method to fetch API results as json.
    :param url: The url to make a POST request to.
    :param headers: Optional headers if additional info needs to be passed along
    :return: The json results or None if error
    """
    if headers is None:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 400:
                    return await resp.json()
                else:
                    return None
    else:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status != 400:
                    return await resp.json()
                else:
                    return None