import os

import requests


def circuit_breaker_base_url():
    return (
            discover_service("circuit-breaker")
            or os.getenv("CB_BASE_URL", "http://localhost:7777")
    )


def discover_service(name, consul_addr=None):
    """Return the base URL for a service registered in Consul."""
    consul_addr = consul_addr or os.getenv("CONSUL_HTTP_ADDR", "http://localhost:8500")
    try:
        return None
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
