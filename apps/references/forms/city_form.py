from django import forms

from apps.references.models.city import City


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name', 'region']
