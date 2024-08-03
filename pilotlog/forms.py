from django import forms
from django.core.exceptions import ValidationError
from .models import FlightLog

class FlightLogForm(forms.ModelForm):
    class Meta:
        model = FlightLog
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        custom_fields = cleaned_data.get('custom_fields', {})
        if 'required_key' not in custom_fields:
            raise ValidationError('Custom fields must include "required_key"')
        return cleaned_data
