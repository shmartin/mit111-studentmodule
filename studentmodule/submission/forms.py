# forms.py
from django import forms
from .models import Program

class SubmissionForm(forms.Form):
    program = forms.ModelChoiceField(
        queryset=Program.objects.all(),
        empty_label="Select a program",
        widget=forms.Select(attrs={'id': 'program', 'required': True})
    )


