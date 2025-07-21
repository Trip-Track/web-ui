import logging

import httpx

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


async def fetch(client: httpx.AsyncClient, key: str, url: str):
    try:
        logger.debug(f"Fetching from {url}")

        resp = await client.get(url, timeout=3)
        resp.raise_for_status()
        return key, resp.json()
    except Exception as exc:

        print(f"[city_info] {key} fetch failed → {exc}")
        return key, None
