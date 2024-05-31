from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["phone_number", "username", "password1", "password2"]
