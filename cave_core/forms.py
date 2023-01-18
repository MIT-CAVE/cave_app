from django import forms
from django.contrib.auth.forms import UserCreationForm
from cave_core import models
from pamda import pamda


@pamda.curry
def user_form_decorator(form_class, globals):
    additional_fields = []
    if globals.allow_user_edit_photo:
        additional_fields += ["photo"]
    if globals.allow_user_edit_bio:
        additional_fields += ["bio"]

    class ModifiedForm(form_class):
        class Meta(form_class.Meta):
            fields = form_class.Meta.fields + additional_fields

    return ModifiedForm


@user_form_decorator()
class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = models.CustomUser
        fields = ["first_name", "last_name"]


class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text="Enter your First Name")
    last_name = forms.CharField(max_length=30, required=True, help_text="Enter your Last Name")

    class Meta:
        model = models.CustomUser
        fields = [
            "username",
            "email",
            "password1",
            "password2",
            "first_name",
            "last_name",
        ]
