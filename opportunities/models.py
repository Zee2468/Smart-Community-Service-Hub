from django.db import models
from django.contrib.auth.models import User


class Opportunity(models.Model):

    CATEGORY_CHOICES = [

        ("Job", "Job"),

        ("Internship", "Internship"),

        ("Learnership", "Learnership"),

        ("Bursary", "Bursary"),

        ("Scholarship", "Scholarship"),

        ("Training", "Training"),

        ("Tender", "Tender"),

        ("Volunteer", "Volunteer"),

    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=200
    )

    company = models.CharField(
        max_length=200
    )

    description = models.TextField()

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES
    )

    location = models.CharField(
        max_length=200
    )

    closing_date = models.DateField()

    apply_link = models.URLField(
        blank=True
    )

    image = models.ImageField(
        upload_to="opportunities/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ["-created_at"]

    def __str__(self):

        return self.title