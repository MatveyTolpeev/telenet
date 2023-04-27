from django import forms
from .models import Service
class ServiceImageSetForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['image']