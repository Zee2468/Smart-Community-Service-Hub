from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):

    title = models.CharField(max_length=200)

    description = models.TextField()

    location = models.CharField(max_length=200)

    event_date = models.DateField()

    event_time = models.TimeField()

    image = models.ImageField(
        upload_to="events/",
        blank=True,
        null=True,
    )

    organizer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["event_date"]

    def __str__(self):
        return self.title