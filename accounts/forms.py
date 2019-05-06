from django import forms
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from django.forms import CharField, SlugField

from .models import CustomUser

studentId = ((2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019))
studentMajor = (('경영정보학과', '경영정보학과'), ('경영학과', '경영학과'), ('국제통상학과', '국제통상학과'), ('회계학과', '회계학과'))


class CustomUserCreationForm(forms.ModelForm):
    studentMajor = forms.ChoiceField(widget=forms.Select, choices=studentMajor, label='전공')
    studentId = forms.ChoiceField(widget=forms.Select, choices=studentId, label='교육과정')
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'studentMajor', 'studentId']


class CustomUserChangeForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'email']