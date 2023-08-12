from django.shortcuts import render
from django.views import View
from library.models import Books
#from .forms import SearchForm
from django.contrib.auth.models import User

class HomePage(View):
    def get(self,request):
        books = Books.objects.all()
        return render(request,'main.html',{'books':books})