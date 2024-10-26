from django.shortcuts import render, redirect
from core.models import Ticket, Flight
from django.http import JsonResponse
import json


def validate_ticket_can_board_flight(ticket, flight):
    if ticket.flight != flight:
        raise BoardingError(f"Ticket {ticket.id} is not for {flight}.")
    if ticket.has_boarded:
        raise BoardingError(f"Ticket {ticket.id} has already boarded.")
    if flight.actual_departure is not None:
        raise BoardingError(f"{flight} has already departed.")
    

class BoardingError(Exception):
    pass
def mark_ticket_as_boarded(ticket_id: int, flight):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        raise BoardingError(f"Ticket with ID {ticket_id} not found.")
    else:
        validate_ticket_can_board_flight(ticket, flight)
        ticket.has_boarded = True
        ticket.save()


def boarding(request, flight_id: int = None):
    if flight_id is None:
        context = {}
        return render(request, "core/boarding.html", context)
    else:
        try:
            flight = Flight.objects.prefetch_related("ticket_set").get(id=flight_id)
        except Flight.DoesNotExist:
            return redirect("/boarding/")
        else:
            context = {"flight": flight}
            if request.method == "POST":
                try:
                    ticket_id = json.loads(request.body)["ticket_id"]
                    mark_ticket_as_boarded(ticket_id, flight)
                except BoardingError as e:
                    return JsonResponse({"success": False, "messages": [str(e)]})
                else:
                    return JsonResponse({"success": True})
            else:
                return render(request, "core/boarding.html", context)
