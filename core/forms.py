from django.contrib.auth.forms import UserCreationForm as UserCreationFormBase
from django import forms
from django.utils.translation import gettext_lazy as _


class UserCreationForm(UserCreationFormBase):
    name = forms.CharField()
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )


class ProfileCreationForm(UserCreationFormBase):
    name = forms.CharField()
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )