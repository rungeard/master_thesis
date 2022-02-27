from django import forms
from hcaptcha_field import hCaptchaField
from .models import *

class Register_form(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control"}))
    hcaptcha = hCaptchaField()

class Login_form(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control"}))
    hcaptcha = hCaptchaField()
