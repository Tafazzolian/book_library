from django import forms

class DateInputForm(forms.Form):
    Return_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

class ReturnBookForm(forms.Form):
    pass

class BuyVip(forms.Form):
    pass