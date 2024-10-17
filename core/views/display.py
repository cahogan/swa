from django.shortcuts import render
from core.models import Flight


def display(request):
    context = {
        "flights": Flight.objects.all() # TODO: Filter out departures that have long since passed
    }
    return render(request, "core/display.html", context)
