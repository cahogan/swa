from django.db import models
from .metadata import Metadata


class Destination(Metadata):
    id = models.AutoField(primary_key=True)

    # Relationships

    # Attributes
    candy = models.CharField(max_length=100)

    def __str__(self):
        return f"Destination {self.id}: {self.candy}"
