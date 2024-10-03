from django.shortcuts import render, redirect
from core.models import Ticket


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
