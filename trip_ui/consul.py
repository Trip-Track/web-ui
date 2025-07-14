import os
from functools import lru_cache

import requests


@lru_cache(maxsize=1)
def trip_planner_base_url():
    return (
            discover_service("trip-planner")
            or os.getenv("API_BASE_URL", "http://localhost:2222")
    )


@lru_cache(maxsize=1)
def city_info_base_url():
    return (
            discover_service("city-info")
            or os.getenv("API_BASE_URL", "http://localhost:2222")
    )


def discover_service(name, consul_addr=None):
    """Return the base URL for a service registered in Consul."""
    consul_addr = consul_addr or os.getenv("CONSUL_HTTP_ADDR", "http://localhost:8500")
    try:
        resp = requests.get(f"{consul_addr}/v1/catalog/service/{name}")
        resp.raise_for_status()
        services = resp.json()
    except Exception:
        return None
    if not services:
        return None
    service = services[0]
    address = service.get("ServiceAddress") or service.get("Address")
    port = service.get("ServicePort")
    if address and port:
        return f"http://{address}:{port}"
    return None
