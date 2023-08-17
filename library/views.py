from django.views import View
from .models import Books,BorrowedBook
from account.models import CustomUser as User
#from django.contrib.auth.models import User as MUser
from datetime import date
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import DateInputForm


class UserProfile(LoginRequiredMixin,View):
    template_class = 'library/user_profile.html'

    def get(self,request, user_id):
        user = User.objects.get(id=user_id)
        borrowed_books = BorrowedBook.objects.filter(user=user.id)
        return render(request,self.template_class,{'borrowed_books': borrowed_books,'user':user})

def ReturnBook(request, borrowed_book_id):
    borrowed_book = get_object_or_404(BorrowedBook, id=borrowed_book_id)
    book = borrowed_book.book
    #borrowed_book.return_date = date.today()
    book.copies_available += 1
    book.save()
    borrowed_book.delete()
    #borrowed_book.save()
    messages.success(request, "You have successfully returned the book.")
    return redirect('library:home')


class BorrowBook(LoginRequiredMixin,View):
    form_class = DateInputForm
    template_class = 'library/borrow.html'
    
    def get(self,request, books_id):
        books = get_object_or_404(Books, id=books_id)
        form = self.form_class()
        return render(request,self.template_class,{'form':form,'books':books})
    
    def post(self,request, books_id):
        form = self.form_class(request.POST)    
        book = get_object_or_404(Books, id=books_id)
        user = User.objects.get(id=request.user.id)
        borrowed_books_count = BorrowedBook.objects.filter(user=user).count()
        if borrowed_books_count >= 5:
            messages.error(request, "You have reached the maximum number of borrowed books.")
        elif book.copies_available <= 0:
            messages.error(request, "No copies of this book are currently available.")
        elif form.is_valid():
            selected_date = form.cleaned_data['Return_date']
            borrowed_book = BorrowedBook(user=user, book=book, borrow_date=date.today(), return_date=selected_date)
            borrowed_book.save()
            book.copies_available -= 1
            book.save()
            messages.success(request, f"You have successfully borrowed '{book.title}'.")
        else:
            self.form_class() 
            
        return redirect('library:home')

class HomePage(View):
    def get(self,request):
        books = Books.objects.all()
        borrowed_books = BorrowedBook.objects.all()
        return render(request,'main.html',{'books':books,'borrowed_books': borrowed_books,})