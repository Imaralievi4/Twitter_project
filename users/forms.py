from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def save(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password1')
        username = self.cleaned_data.get('username')
        user = get_user_model().object.create_user(email=email, password=password, username=username)
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['avatar']