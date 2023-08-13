from django.views import View
from library.models import Books,BorrowedBook
from django.contrib.auth.models import User
from datetime import date
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import DateInputForm



class BorrowBook(View):
    form_class = DateInputForm
    
    def get(self,request, books_id):
        get_object_or_404(Books, id=books_id)
        form = self.form_class()
        return render(request,'main.html',{'form':form})
    
    @login_required
    def post(self,request, books_id):
        form = self.form_class(request.POST)    
        book = get_object_or_404(Books, id=books_id)
        user = User.objects.get(id=user_id)
        borrowed_books_count = BorrowedBook.objects.filter(user=user).count()
        if borrowed_books_count >= 5:
            messages.error(request, "You have reached the maximum number of borrowed books.")
        elif book.copies_available <= 0:
            messages.error(request, "No copies of this book are currently available.")
        elif form.is_valid():
            selected_date = form.cleaned_data['date']
            borrowed_book = BorrowedBook(user=user, book=book, borrow_date=date.today(), return_date=selected_date)
            borrowed_book.save()
            book.copies_available -= 1
            book.save()
            messages.success(request, f"You have successfully borrowed '{book.title}'.")
                # Do something with the selected_date
        else:
            self.form_class() 
            
        return render(request,'main.html',{'form':form})
        #return redirect('library:home')

@login_required
def return_book(request, borrowed_book_id):
    borrowed_book = get_object_or_404(BorrowedBook, id=borrowed_book_id)

    # Set the return date and increase the available copies
    borrowed_book.return_date = date.today()
    borrowed_book.book.copies_available += 1

    borrowed_book.book.save()
    borrowed_book.save()
    messages.success(request, "You have successfully returned the book.")

    return redirect('library:home')

class HomePage(View):
    def get(self,request):
        books = Books.objects.all()
        borrowed_books = BorrowedBook.objects.all()
        return render(request,'main.html',{'books':books,'borrowed_books': borrowed_books,})