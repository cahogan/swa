from django.urls import path
import core.views
from django.conf.urls.static import static
from django.conf import settings


app_name = "core"

urlpatterns = [
    path("", core.views.home, name="home"),
    path("ticket/", core.views.ticket, name="ticket"),
    path("ticket/<int:ticket_id>/", core.views.ticket, name="ticket"),
    path("ticket/<int:ticket_id>/print/", core.views.print_ticket, name="print_ticket"),
    path("book/", core.views.book_ticket, name="book"),
    path("flight/", core.views.flight, name="flight"),
    path("flight/<int:flight_id>/", core.views.flight, name="flight"),
    path("flight/<int:flight_id>/takeoff/", core.views.takeoff, name="takeoff"),
    path("display/", core.views.display, name="display"),
    path("boarding/", core.views.boarding, name="boarding"),
    path("boarding/<int:flight_id>/", core.views.boarding, name="boarding"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
