from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class UserRegistrationForm(UserCreationForm):
    """Form for register user"""
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', 'password1', 'password2')

    def save(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password1')
        user = get_user_model().object.create_user(email=email, password=password)
        #MyUser.object.create_user
        return user