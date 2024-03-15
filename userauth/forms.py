from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User

form_field_class = "form-control w-75 my-2 p-2 border shadow-sm"


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Username",
        'class': form_field_class,
    }))

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'email',
        'class': form_field_class,
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': form_field_class,
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': form_field_class,
    }))
