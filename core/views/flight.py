from django.shortcuts import render, redirect
from core.models import Flight


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
        else:
            context["flight"] = flight
        return render(request, "core/flight.html", context)
