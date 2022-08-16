# from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from django.forms.widgets import TextInput
from cave_core import models


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = models.CustomUser
        fields = "__all__"


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = models.CustomUser
        fields = "__all__"


class GlobalsForm(ModelForm):
    class Meta:
        model = models.Globals
        fields = "__all__"
        widgets = {
            "primary_color": TextInput(attrs={"type": "color"}),
            "secondary_color": TextInput(attrs={"type": "color"}),
        }
