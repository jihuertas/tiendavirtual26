from django.forms import Form
from django import forms

class CheckoutForm(Form):
    unidades = forms.IntegerField()
    codigo = forms.CharField(max_length=10, required=False)
