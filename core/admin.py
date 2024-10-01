from django.contrib import admin
from core.models import Destination, Gate, Flight, Ticket

admin.site.register(Destination)
admin.site.register(Gate)
admin.site.register(Flight)
admin.site.register(Ticket)
