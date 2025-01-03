from django import forms
from .models import MoneySource

class MoneySourceForm(forms.ModelForm):
    class Meta:
        model = MoneySource
        fields = ['name', 'balance', 'source_type']