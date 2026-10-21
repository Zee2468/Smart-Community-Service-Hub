from django import forms
from .models import Event


class EventForm(forms.ModelForm):

    class Meta:

        model = Event

        fields = [
            "title",
            "description",
            "location",
            "event_date",
            "event_time",
            "image",
        ]

        widgets = {

            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Event title"
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Describe the event..."
            }),

            "location": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Location"
            }),

            "event_date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control",
            }),

            "event_time": forms.TimeInput(attrs={
                "type": "time",
                "class": "form-control",
            }),

            "image": forms.ClearableFileInput(attrs={
                "class": "form-control",
            }),
        }