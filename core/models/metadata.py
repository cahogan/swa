from django.db import models
from django.utils import timezone


class Metadata(models.Model):
    id = models.AutoField(primary_key=True)

    # Attributes
    date_created = models.DateTimeField(editable=False)
    date_modified = models.DateTimeField()
    data_source = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        """
        When the model is saved, set date_created if it is
        the first save, and update date_modified to the current
        time.
        """
        now = timezone.now()
        if self._state.adding:
            self.date_created = now
        self.date_modified = now
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}"

    class Meta:
        abstract = True
