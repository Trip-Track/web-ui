import asyncio
import logging

import httpx
import requests
from django.http import JsonResponse
from django.shortcuts import render

from trip_ui.consul import circuit_breaker_base_url
from trip_ui.view_helpers.city_info import fetch

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def index(request):
    """Render landing page."""
    logger.debug("Rendering index page")
    return render(request, "trip_ui/index.html")


def graph_data(request):
    """Return data for the network graph widget."""
    logger.info("Fetching graph data")
    data: dict = {}
    try:
        base = circuit_breaker_base_url()
        resp = requests.get(f"{base}/map", timeout=5)
        resp.raise_for_status()
        data = resp.json()
        logger.debug("Graph data retrieved successfully – %s keys", len(data))
    except Exception:
        logger.exception("Failed to retrieve graph data from %s", base)
    return JsonResponse(data)


def trip_path(request):
    """Return an optimal trip path between two cities."""
    base = circuit_breaker_base_url()
    start = request.GET.get("start")
    end = request.GET.get("end")
    logger.info("Calculating trip path | start=%s end=%s", start, end)

    if not start or not end:
        logger.warning("Missing start or end query param: start=%s end=%s", start, end)
        return JsonResponse({"error": "start and end required"}, status=400)

    try:
        resp = requests.get(
            f"{base}/trip", params={"from": start, "to": end}, timeout=5
        )
        resp.raise_for_status()
        data = resp.json()
        logger.debug("Trip path retrieved – %s stops", len(data.get("stops", [])))
    except Exception:
        logger.exception("Failed to retrieve trip path: start=%s end=%s", start, end)
        data = {"cost": float("nan"), "stops": []}
    return JsonResponse(data)


async def city_info(request):
    """Asynchronously gather multiple pieces of information about a city."""
    base = circuit_breaker_base_url()
    city = request.GET.get("city")
    logger.info("Fetching city info for '%s'", city)

    if not city:
        logger.warning("Missing required query param: city")
        return JsonResponse({"error": "Missing required query param: city"}, status=400)

    endpoints = {
        "area": f"{base}/city/{city}/area",
        "population": f"{base}/city/{city}/population",
        "fun_fact": f"{base}/city/{city}/fun-fact",
    }

    async with httpx.AsyncClient() as client:
        tasks = [fetch(client, key, url) for key, url in endpoints.items()]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    data: dict = {}
    for result in results:
        if isinstance(result, Exception):
            logger.exception("Error fetching one of the city endpoints for '%s'", city)
            continue
        key, payload = result
        data[key] = payload

    logger.debug("City info assembled for '%s' – %s fields", city, data.keys())
    return JsonResponse(data)
