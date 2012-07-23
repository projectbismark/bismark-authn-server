#-*- coding: utf-8 -*-

from django import forms

class AuthorizeForm(forms.Form):
    pass

class InfoForm(forms.Form):
    isp = forms.CharField(label="ISP", max_length=75, widget=forms.TextInput(attrs=dict(maxlength=75)))
    service_type = forms.ChoiceField(label="Service Type", choices=(('1', 'DSL'), ('2', 'Fiber'), ('3', 'Cable'), ('4', 'Wireless- Cellular'), ('5', 'Wireless- WiMAX'), ('6', 'Wireless- 802.11'), ('7', 'Other')))
    service_plan = forms.CharField(label="Service Plan", max_length=75, widget=forms.TextInput(attrs=dict(maxlength=75)))
    drate = forms.IntegerField(label="Download Rate")
    urate = forms.IntegerField(label="Upload Rate")
    location = forms.CharField(label="City", max_length=75, widget=forms.TextInput(attrs=dict(maxlength=75)))
