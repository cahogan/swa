from django.shortcuts import render, redirect
from core.models import Ticket, Flight
from django.db.models import F


# Check a customer's flight status 
def ticket(request, ticket_id: int = None):
    if ticket_id is None and request.method == "POST":
        ticket_id = request.POST.get("id")
        redirect_url = f"/ticket/{ticket_id}/"
        return redirect(redirect_url)
    else:
        context = {}
        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            ticket = None
        else:
            context["ticket"] = ticket
        return render(request, "core/ticket.html", context)


def get_boarding_position(current_bookings: int):
    group = chr((current_bookings // 10) + 65)
    number = (current_bookings % 10) + 1
    return group, number


def book_ticket(request):
    if request.method == "POST":
        try:
            flight = Flight.objects.prefetch_related("ticket_set").get(id=request.POST.get("flight_id"))
        except Flight.DoesNotExist:
            return redirect("/book/") #TODO: Add error message
        else:
            current_bookings = flight.ticket_set.count()
            checkbox = True if request.POST.get("tsa_precheck") is not None else False
            if current_bookings < flight.capacity:
                group, number = get_boarding_position(current_bookings)
                ticket = Ticket.objects.create(
                    flight=flight,
                    first_name=request.POST.get("customer_name"),
                    costume=request.POST.get("customer_costume"),
                    tsa_precheck=checkbox,
                    boarding_group=group,
                    boarding_position=number,
                )
                ticket.save()
            else:
                return redirect("/book/") #TODO: Add error message
        return redirect(f"/ticket/{ticket.id}/")
    else:
        available_flights = Flight.objects.filter(actual_departure__isnull=True)
        context = {"flights": available_flights}
        return render(request, "core/booking.html", context)
