#-*- coding: utf-8 -*-

from django import forms
from django_countries.countries import COUNTRIES

class AuthorizeForm(forms.Form):
    pass

class InfoForm(forms.Form):
    isp = forms.CharField(label="Internet Service Provider (ISP)", max_length=75, widget=forms.TextInput(attrs=dict(maxlength=75)))
    service_type = forms.ChoiceField(label="Service Type", choices=(('DSL', 'DSL'), ('Fiber', 'Fiber'), ('Cable', 'Cable'), ('Wireless-Cellular', 'Wireless- Cellular'), ('Wireless- WiMAX', 'Wireless- WiMAX'), ('Wireless-802.11', 'Wireless- 802.11'), ('Other', 'Other')))
    service_plan = forms.CharField(label="Service Plan", max_length=75, widget=forms.TextInput(attrs=dict(maxlength=75)))
    drate = forms.IntegerField(label="Download Rate (Kb/s)", required=False)
    urate = forms.IntegerField(label="Upload Rate (Kb/s)", required=False)
    city = forms.CharField(label="City", max_length=75, widget=forms.TextInput(attrs=dict(maxlength=75)))
    state = forms.CharField(label="State", max_length=75, widget=forms.TextInput(attrs=dict(maxlength=75)))
    country = forms.ChoiceField(label="Country", choices=COUNTRIES)
