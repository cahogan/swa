from django.db import models
from .metadata import Metadata
from zoneinfo import ZoneInfo


class Flight(Metadata):
    id = models.AutoField(primary_key=True)

    # Relationships
    gate = models.ForeignKey("Gate", on_delete=models.PROTECT)
    destination = models.ForeignKey("Destination", on_delete=models.PROTECT)

    # Attributes
    scheduled_departure = models.DateTimeField(blank=True, null=True)
    scheduled_arrival = models.DateTimeField(blank=True, null=True)
    delay_minutes = models.IntegerField(blank=True, null=True)
    actual_departure = models.DateTimeField(blank=True, null=True)
    actual_arrival = models.DateTimeField(blank=True, null=True)
    capacity = models.IntegerField()

    def __str__(self):
        adjusted_for_timezone = self.scheduled_departure.astimezone(ZoneInfo('America/Los_Angeles'))
        return f"Flight {self.id}: {self.destination} at {adjusted_for_timezone.strftime('%H:%M %z')}"
