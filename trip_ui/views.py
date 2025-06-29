from django.shortcuts import render


def index(request):
    context = {"map": 5}

    return render(request, "polls/index.html", context)
