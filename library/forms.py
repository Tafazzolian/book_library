from django import forms
from .models import Books

class DateInputForm(forms.Form):
    Return_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

class ReturnBookForm(forms.Form):
    pass

class BooksCrudForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = '__all__'

class WalletChargeForm(forms.Form):
    amount = forms.IntegerField(widget=forms.NumberInput(attrs={'type':'number'}))