from .models import Books, BorrowedBook, Transaction, Genre, Author
from account.models import CustomUser as User
from django.shortcuts import get_object_or_404

class Model:

    @staticmethod
    def get(model,id):
        data = model.objects.get(pk=id)
        return data
    
    @staticmethod
    def save(model):
        model.save()

    @staticmethod
    def delete(model):
        model.delete()

    @staticmethod
    def all(model):
        data = model.objects.all()
        return data
    
    @staticmethod
    def filter(model,*args):
        data = model.objects.filter(args)
        return data

    