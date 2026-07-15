from django import forms
from .models import Opportunity


class OpportunityForm(forms.ModelForm):

    class Meta:

        model = Opportunity

        fields = [

            "title",

            "company",

            "description",

            "category",

            "location",

            "closing_date",

            "apply_link",

            "image",

        ]

        widgets = {

            "title": forms.TextInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "Opportunity Title"

                }

            ),

            "company": forms.TextInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "Company or Organisation"

                }

            ),

            "description": forms.Textarea(

                attrs={

                    "class": "form-control",

                    "rows": 5,

                    "placeholder": "Describe this opportunity..."

                }

            ),

            "category": forms.Select(

                attrs={

                    "class": "form-select"

                }

            ),

            "location": forms.TextInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "Location"

                }

            ),

            "closing_date": forms.DateInput(

                attrs={

                    "class": "form-control",

                    "type": "date"

                }

            ),

            "apply_link": forms.URLInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "https://example.com"

                }

            ),

            "image": forms.FileInput(

                attrs={

                    "class": "form-control"

                }

            ),

        }