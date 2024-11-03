from django.shortcuts import render
from core.models import Flight
from datetime import timedelta
from zoneinfo import ZoneInfo
from django.http import JsonResponse
from datetime import datetime


def add_status(flight):
    now = datetime.now(tz=ZoneInfo('America/Los_Angeles'))
    flight_is_delayed = flight.delay_minutes is not None
    flight_has_departed = flight.actual_departure is not None
    if flight_has_departed:
        flight.status = "Departed"
    else:
        updated_departure = flight.scheduled_departure + timedelta(minutes=flight.delay_minutes) if flight_is_delayed else flight.scheduled_departure
        time_until_departure = updated_departure - now
        if time_until_departure < timedelta(minutes=1):
            flight.status = "Final Call"
        elif time_until_departure < timedelta(minutes=15):
            flight.status = "Boarding"
        elif flight_is_delayed:
            flight.status = "Delayed"
        else:
            flight.status = "On Time"
    return flight


def add_available_seats(flight):
    flight.available_seats = f"{flight.ticket_set.count()} / {flight.capacity}"
    return flight


def flight_serializer(flight):
    updated_departure = flight.scheduled_departure + timedelta(minutes=flight.delay_minutes) if flight.delay_minutes is not None else flight.scheduled_departure
    return {
        "id": flight.id,
        "candy_image": flight.destination.candy.logo.url,
        "destination": str(flight.destination),
        "scheduled_departure": updated_departure.astimezone(ZoneInfo('America/Los_Angeles')).strftime("%I:%M %p"),
        "gate": str(flight.gate),
        "updated_departure": flight.scheduled_departure.astimezone(ZoneInfo('America/Los_Angeles')).strftime("%I:%M %p"),
        "available_seats": flight.available_seats,
        "status": flight.status
    }


def display(request):
    flights = Flight.objects.filter(actual_departure__isnull=True)
    flights_augmented = [add_available_seats(add_status(flight)) for flight in flights]
    context = {
        "flights": flights_augmented # TODO: Filter out departures that have long since passed
    }
    if request.method == "POST":
        serialized_flights = [flight_serializer(flight) for flight in flights_augmented]
        return JsonResponse({"flights": serialized_flights})
    else:
        return render(request, "core/display.html", context)

