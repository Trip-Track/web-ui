import httpx


async def fetch(client: httpx.AsyncClient, key: str, url: str):
    try:
        resp = await client.get(url, timeout=3)
        resp.raise_for_status()
        return key, resp.json()
    except Exception as exc:

        print(f"[city_info] {key} fetch failed → {exc}")
        return key, None
