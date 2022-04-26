from django import forms
from django.core.exceptions import ValidationError

from dbcanary.models import ENGINE_TYPE, DRIVE, GEAR_BOX, ORDER_BY_CHOICES


class CarFiltersForm(forms.Form):
    price__gt = forms.IntegerField(min_value=0, label="Price Min", required=False)
    price__lt = forms.IntegerField(min_value=0, label="Price Max", required=False)
    order_by = forms.ChoiceField(choices=ORDER_BY_CHOICES, required=False)
    engine_type = forms.ChoiceField(choices=ENGINE_TYPE, required=False,)
    gear_box = forms.ChoiceField(choices=GEAR_BOX, required=False)
    drive = forms.ChoiceField(choices=DRIVE, required=False)

    def clean(self):
        cleaned_data = super().clean()
        price__gt = cleaned_data.get("price__gt")
        price__lt = cleaned_data.get("price__lt")
        if price__gt and price__lt and price__gt > price__lt:
            raise ValidationError("Min price can't be greater than Max price")


class AdvertForm(forms.Form):
    engine_type = forms.ChoiceField(choices=ENGINE_TYPE)
    engine_capacity = forms.DecimalField(decimal_places=2, max_digits=15)
    drive = forms.ChoiceField(choices=DRIVE)
    gear_box = forms.ChoiceField(choices=GEAR_BOX)
    description = forms.CharField(max_length=500)
    image = forms.ImageField(required=False)
    win = forms.CharField(max_length=17,)
    price = forms.DecimalField(decimal_places=2, max_digits=15)
    price_usd = forms.DecimalField(decimal_places=2, max_digits=15)
    phone_number = forms.CharField(max_length=13)
