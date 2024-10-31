from django.shortcuts import render, redirect
from django.http import JsonResponse
from core.models import Ticket, Flight
from label_printer.label_printer.boarding_pass_printer import generate_boarding_pass, print_boarding_pass
from io import BytesIO
from django.core.files import File
from PIL import Image
from django.db import transaction
from django.db.models import Count


def generate_boarding_pass_for_ticket(ticket_id: int):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        raise ValueError(f"Ticket with ID {ticket_id} does not exist.")
    image = generate_boarding_pass(
                    ticket_id=ticket.id,
                    lastname=ticket.costume,
                    firstname=ticket.first_name,
                    gate=ticket.flight.gate.id,
                    departure_datetime=ticket.flight.scheduled_departure,
                    boarding_datetime=ticket.flight.scheduled_departure,
                    confirmation_number="AWGLUD",
                    departure_airport_code="ARB",
                    departure_airport_city="Los Altos",
                    departure_airport_name="Arbor Aveport",
                    arrival_airport_city=ticket.flight.destination.name,
                    arrival_airport_name=ticket.flight.destination.candy.name,
                    arrival_airport_code=ticket.flight.destination.code,
                    flight_number=ticket.flight.id,
                    boarding_group=ticket.boarding_group,
                    boarding_position=ticket.boarding_position
                )
    blob = BytesIO()
    image.save(blob, 'JPEG')  
    ticket.boarding_pass_preview.save(f'ticket-{ticket.id}.jpg', File(blob), save=False)
    ticket.save()


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
            if not ticket.boarding_pass_preview:
                generate_boarding_pass_for_ticket(ticket.id)
                ticket.refresh_from_db()
            context["ticket"] = ticket
        return render(request, "core/ticket.html", context)


def get_boarding_position(current_bookings: int):
    group = chr((current_bookings // 9) + 65)
    number = (current_bookings % 9) + 1
    return group, number


def book_ticket(request):
    if request.method == "POST":
        with transaction.atomic():
            try:
                flight = Flight.objects.select_for_update().prefetch_related("ticket_set").get(id=request.POST.get("flight_id"))
            except Flight.DoesNotExist:
                return redirect("/book/") #TODO: Add error message
            else:
                current_bookings = flight.ticket_set.count()
                checkbox = True if request.POST.get("standby") is not None else False
                if current_bookings < flight.capacity:
                    group, number = get_boarding_position(current_bookings)
                    ticket = Ticket.objects.create(
                        flight=flight,
                        first_name=request.POST.get("customer_name"),
                        costume=request.POST.get("customer_costume"),
                        standby=checkbox,
                        boarding_group=group,
                        boarding_position=number,
                    )
                    ticket.save()
                    generate_boarding_pass_for_ticket(ticket.id)
                else:
                    return redirect("/book/") #TODO: Add error message
        return redirect(f"/ticket/{ticket.id}/")
    else:
        available_flights = Flight.objects.filter(actual_departure__isnull=True).annotate(num_tickets=Count("ticket"))
        flights_with_capacity = [flight for flight in available_flights if flight.num_tickets < flight.capacity]
        context = {"flights": flights_with_capacity}
        return render(request, "core/booking.html", context)
    

def print_ticket(request, ticket_id: int):
    if request.method == "POST":
        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            return JsonResponse({
                "success": False,
                "error": f"Ticket with ID {ticket_id} does not exist."
                })
        else:
            pil_image = Image.open(ticket.boarding_pass_preview)
            print_boarding_pass(pil_image)
            return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False, "error": "Invalid request method."})
