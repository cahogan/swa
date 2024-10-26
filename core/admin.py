from django.contrib import admin
from core.models import Destination, Gate, Flight, Ticket, CandyType

admin.site.register(Destination)
admin.site.register(Gate)
admin.site.register(Flight)
admin.site.register(Ticket)
admin.site.register(CandyType)
