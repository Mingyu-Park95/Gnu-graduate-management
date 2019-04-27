from django import forms
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.validators import RegexValidator

from django.forms import CharField, SlugField

from .models import CustomUser


class CustomUserCreationForm(forms.ModelForm):

    password = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    # username = forms.CharField(validators=[RegexValidator(regex='a-zA-Z0-9')])

    class Meta:
        model = CustomUser
        fields = ['username', 'studentId', 'studentMajor', 'email']


class CustomUserChangeForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'email']