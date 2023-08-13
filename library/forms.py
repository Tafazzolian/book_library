from django import forms

class DateInputForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))