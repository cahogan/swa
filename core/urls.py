from django.urls import path
import core.views


app_name = "core"

urlpatterns = [
    path("", core.views.home, name="home"),
    path("ticket/", core.views.ticket, name="ticket"),
    path("ticket/<int:ticket_id>/", core.views.ticket, name="ticket"),
    path("flight/", core.views.flight, name="flight"),
    path("flight/<int:flight_id>/", core.views.flight, name="flight"),
]
