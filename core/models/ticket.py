from django.db import models
from .metadata import Metadata


class Ticket(Metadata):
    id = models.AutoField(primary_key=True)

    # Relationships
    flight = models.ForeignKey("Flight", on_delete=models.PROTECT)

    # Attributes
    first_name = models.CharField(max_length=100)
    costume = models.CharField(max_length=100)
    tsa_precheck = models.BooleanField()
    boarding_group = models.CharField(max_length=1)
    boarding_position = models.IntegerField()
    has_boarded = models.BooleanField(default=False)
    boarding_pass_preview = models.ImageField(upload_to="boarding_passes", blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.costume} on {self.flight}"
