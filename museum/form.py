from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Location


class LogUploadForm(forms.ModelForm):
    log = forms.FileInput()

    #class Meta:
      #  fields = [' ']