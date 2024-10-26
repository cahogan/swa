from django.db import models
from .metadata import Metadata


class Gate(Metadata):
    id = models.AutoField(primary_key=True)

    # Relationships

    # Attributes
    order = models.IntegerField()

    def __str__(self):
        return f"Gate {self.id}"
