import os

from django.http import JsonResponse
from django.shortcuts import render
import requests

TRIP_PLANNER_API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8089")


def index(request):
    return render(request, "trip_ui/index.html")


def graph_data(request):
    try:
        resp = requests.get(f"{TRIP_PLANNER_API_BASE_URL}/map")
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        data = {
            "connections": [
                {
                    "id": {"code": "A", "name": "A", "lat": 0.5, "lng": 0.5},
                    "from": {"code": "A", "name": "A", "lat": 0.5, "lng": 0.5},
                    "to": {"code": "B", "name": "B", "lat": 0, "lng": 1},
                    "weight": 1,
                },
                {
                    "id": {"code": "A", "name": "A", "lat": 0.5, "lng": 0.5},
                    "from": {"code": "A", "name": "A", "lat": 0.5, "lng": 0.5},
                    "to": {"code": "C", "name": "C", "lat": 1, "lng": 0},
                    "weight": 1,
                },
            ]
        }
    return JsonResponse(data)


def path(request):
    start = request.GET.get("start")
    end = request.GET.get("end")
    if not start or not end:
        return JsonResponse({"error": "start and end required"}, status=400)
    try:
        resp = requests.get(f"{TRIP_PLANNER_API_BASE_URL}/plan", params={"from": start, "to": end})
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(e)
        data = {
            "cost": float("nan"),
            "stops": []
        }
    return JsonResponse(data)
