import asyncio

import httpx
import requests
from django.http import JsonResponse
from django.shortcuts import render

from trip_ui.consul import city_info_base_url, trip_planner_base_url
from trip_ui.view_helpers.city_info import fetch


def index(request):
    return render(request, "trip_ui/index.html")


def graph_data(request):
    data = {}
    try:
        base = trip_planner_base_url()
        resp = requests.get(f"{base}/map")
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(e)
    return JsonResponse(data)


def trip_path(request):
    base = trip_planner_base_url()
    start = request.GET.get("start")
    end = request.GET.get("end")
    if not start or not end:
        return JsonResponse({"error": "start and end required"}, status=400)
    try:
        resp = requests.get(f"{base}/trip", params={"from": start, "to": end})
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(e)
        data = {
            "cost": float("nan"),
            "stops": []
        }
    return JsonResponse(data)


async def city_info(request):
    base = city_info_base_url().rstrip("/")
    city = request.GET.get("city")

    if not city:
        return JsonResponse(
            {"error": "Missing required query param: city"}, status=400
        )

    endpoints = {
        "area": f"{base}/city/{city}/area",
        "population": f"{base}/city/{city}/population",
        "fun_fact": f"{base}/city/{city}/fun-fact",
    }

    async with httpx.AsyncClient() as client:
        tasks = [fetch(client, key, url) for key, url in endpoints.items()]
        results = await asyncio.gather(*tasks)

    data = {key: payload for key, payload in results}
    return JsonResponse(data)
