from django.db import models
from .metadata import Metadata


class CandyType(Metadata):
    id = models.AutoField(primary_key=True)

    # Relationships

    # Attributes
    name = models.CharField(max_length=100)
    current_stock = models.IntegerField()
    
    def __str__(self):
        return f"{self.name}"


class Destination(Metadata):
    id = models.AutoField(primary_key=True)

    # Relationships
    candy = models.ForeignKey("CandyType", on_delete=models.PROTECT)
    code = models.CharField(max_length=3, blank=True, null=True)

    # Attributes
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} ({self.candy})"
