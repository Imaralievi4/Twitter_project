from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    # password = forms.CharField(min_length=8, required=True, widget=forms.PasswordInput)
    # password_confirmation = forms.CharField(min_length=8, required=True, widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     if User.objects.filter(username=username).exists():
    #         raise forms.ValidationError('User with given username already exists')
    #     return username

    # def clean(self):
    #     data = self.cleaned_data
    #     password = data.get('password')
    #     password_confirmation = data.pop('password_confirmation')
    #     if password != password_confirmation:
    #         raise forms.ValidationError('Пароли не совпадают')
    #     return data

    def save(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password1')
        username = self.cleaned_data.get('username')
        user = get_user_model().object.create_user(email=email, password=password, username=username)
        #MyUser.object.create_user
        return user


# class CustomUserChangeForm(UserChangeForm):

#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email', 'password1', 'password2')