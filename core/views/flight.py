from django.shortcuts import render, redirect
from core.models import Flight
from .display import add_status
import datetime


def mark_flight_as_departed(flight):
    flight.actual_departure = datetime.datetime.now()
    flight.save()


def takeoff(request, flight_id: int):
    try:
        flight = Flight.objects.get(id=flight_id)
    except Flight.DoesNotExist:
        return redirect("/flight/")
    else:
        mark_flight_as_departed(flight)
        return redirect("/flight/")


# Adjust flight capacity or timing 
def flight(request, flight_id: int = None):
    if flight_id is None and request.method == "POST":
        flight_id = request.POST.get("id")
        redirect_url = f"/flight/{flight_id}/"
        return redirect(redirect_url)
    else:
        context = {}
        try:
            flight = Flight.objects.get(id=flight_id)
        except Flight.DoesNotExist:
            flight = None
            flight_list = Flight.objects.all()
            flight_list_augmented = [add_status(flight) for flight in flight_list]
            context["flight_list"] = flight_list_augmented
        else:
            context["flight"] = flight
        return render(request, "core/flight.html", context)
