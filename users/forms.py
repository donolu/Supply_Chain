from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms


class RegisterCustomerForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "username", "first_name", "last_name"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "username",
            "profile_image",
        ]
