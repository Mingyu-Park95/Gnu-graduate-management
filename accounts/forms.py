from django import forms
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from django.forms import CharField, SlugField

from .models import CustomUser

eduYear = ((2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019))
studentMajor = (('경영정보학과', '경영정보학과'), ('경영학과', '경영학과'), ('국제통상학과', '국제통상학과'), ('회계학과', '회계학과'))
studentDoubleMajor = (('해당없음', '해당없음'), ('경영정보학과', '경영정보학과'), ('경영학과', '경영학과'),
                     ('국제통상학과', '국제통상학과'), ('회계학과', '회계학과'))
studentTrack = (('해당없음', '해당없음'), ('재무금융트랙', '재무금융트랙'), ('세무전문트랙', '세무전문트랙'),
                ('유통서비스트랙', '유통서비스트랙'), ('IT융합시스템개발', 'IT융합시스템개발'))
studentSubMajor = (('해당없음', '해당없음'), ('경영정보학과', '경영정보학과'), ('경영학과', '경영학과'),
                     ('국제통상학과', '국제통상학과'), ('회계학과', '회계학과'))
studentConvergenceMajor = (('해당없음', '해당없음'),  ('산업경영지원학', '산업경영지원학'))
studentTeaching = (('해당없음', '해당없음'), ('해당', '해당'))

# studentDoubleMajor = models.CharField(max_length=30, default=None, null=True)
#     studentTrack = models.CharField(max_length=30, default=None, null=True)
#     studentSubMajor = models.CharField(max_length=30, default=None, null=True)
#     studentConvergenceMajor = models.CharField(max_length=30, default=None, null=True)
#     studentTeaching = models.CharField(max_length=30, default=None, null=True) # 교직이수


class CustomUserCreationForm(forms.ModelForm):
    studentMajor = forms.ChoiceField(widget=forms.Select, choices=studentMajor, label='전공')
    eduYear = forms.ChoiceField(widget=forms.Select, choices=eduYear, label='교육과정')

    studentDoubleMajor = forms.ChoiceField(widget=forms.Select, choices=studentDoubleMajor, label='복수전공')
    studentTrack = forms.ChoiceField(widget=forms.Select, choices=studentTrack, label='트랙제')
    studentSubMajor = forms.ChoiceField(widget=forms.Select, choices=studentSubMajor, label='부전공')
    studentConvergenceMajor = forms.ChoiceField(widget=forms.Select, choices=studentConvergenceMajor, label='융합전공')
    studentTeaching = forms.ChoiceField(widget=forms.Select, choices=studentTeaching, label='교직이수')

    password = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)


    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'studentMajor', 'eduYear', 'studentDoubleMajor', 'studentTrack',
                  'studentSubMajor', 'studentConvergenceMajor', 'studentTeaching']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다')
        return cd['password2']


class CustomUserChangeForm(forms.ModelForm):
    studentMajor = forms.ChoiceField(widget=forms.Select, choices=studentMajor, label='전공')
    studentId = forms.ChoiceField(widget=forms.Select, choices=eduYear, label='교육과정')
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        exclude = ['username']
        fields = ['email', 'studentMajor', 'eduYear', 'studentDoubleMajor', 'studentTrack',
                  'studentSubMajor', 'studentConvergenceMajor', 'studentTeaching']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다')
        return cd['password2']
