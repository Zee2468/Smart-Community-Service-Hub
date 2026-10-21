from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Opportunity


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):

    list_display = (

        "title",

        "company",

        "category",

        "location",

        "closing_date",

    )

    search_fields = (

        "title",

        "company",

        "location",

    )

    list_filter = (

        "category",

        "closing_date",

    )