from django import forms
from .models import Issue


class IssueForm(forms.ModelForm):

    class Meta:
        model = Issue
        fields = [
            'title',
            'description',
            'category',
            'location',
            'image',
        ]

        widgets = {
    'title': forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter issue title'
        }
    ),

    'description': forms.Textarea(
        attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Describe the issue in detail'
        }
    ),

    'category': forms.Select(
        attrs={
            'class': 'form-select'
        }
    ),

    'location': forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter location'
        }
    ),

    'image': forms.FileInput(
        attrs={
            'class': 'form-control'
        }
    ),
}