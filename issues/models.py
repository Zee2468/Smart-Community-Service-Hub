from django.db import models
from django.contrib.auth.models import User


class Issue(models.Model):

    CATEGORY_CHOICES = [
        ('Water', 'Water'),
        ('Electricity', 'Electricity'),
        ('Roads', 'Roads'),
        ('Crime', 'Crime'),
        ('Dumping', 'Illegal Dumping'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )
    location = models.CharField(max_length=200)

    image = models.ImageField(
        upload_to='issues/',
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title