from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("graph-data/", views.graph_data, name="graph_data"),
    path("path/", views.trip_path, name="path"),
    path("city_info/", views.city_info, name="city_info")
]
