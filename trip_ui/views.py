
from django.http import JsonResponse
from django.shortcuts import render
import requests
from .consul import trip_planner_base_url



def index(request):
    return render(request, "trip_ui/index.html")


def graph_data(request):
    try:
        base = trip_planner_base_url()
        resp = requests.get(f"{base}/map")
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
    base = trip_planner_base_url()
    start = request.GET.get("start")
    end = request.GET.get("end")
    if not start or not end:
        return JsonResponse({"error": "start and end required"}, status=400)
    try:
        resp = requests.get(f"{base}/plan", params={"from": start, "to": end})
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(e)
        data = {
            "cost": float("nan"),
            "stops": []
        }
    return JsonResponse(data)
