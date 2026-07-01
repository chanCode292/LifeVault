from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your first name'
        })
    )

    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your last name'
        })
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your username'
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email'
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Create a password'
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm your password'
        })
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2'
        ]