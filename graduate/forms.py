from django import forms

class SearchForm(forms.ModelForm):
    choices = forms.MultipleChoiceField(
         # this is optional
        widget=forms.CheckboxSelectMultiple,
    )