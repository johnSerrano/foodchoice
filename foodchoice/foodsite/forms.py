from django import forms

class RequestForm(forms.Form):
    location = forms.CharField(label="Restaurant", max_length=50)
