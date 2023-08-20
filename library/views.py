from django.views import View
from .models import Books,BorrowedBook, Genre, Author
from account.models import CustomUser as User
#from django.contrib.auth.models import User as MUser
from datetime import date, timedelta
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import DateInputForm
from django.db.models import Q
from django.core.paginator import Paginator


class UserProfile(LoginRequiredMixin,View):
    template_class = 'library/user_profile.html'

    def get(self,request, user_id):
        user = User.objects.get(id=user_id)
        borrowed_books = BorrowedBook.objects.filter(user=user.id)
        for i in borrowed_books:
            if date.today()-i.borrow_date >= timedelta(days=7):
                i.date_check = True
            else:
                i.date_check = False
                i.save()
                continue

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


class BorrowBook(View):
    form_class = DateInputForm
    template_class = 'library/borrow.html'
    
    def get(self,request, books_id):
        books = get_object_or_404(Books, id=books_id)
        form = self.form_class()
        return render(request,self.template_class,{'form':form,'book':books})
    
    def post(self,request, books_id):
        form = self.form_class(request.POST)    
        book = get_object_or_404(Books, id=books_id)
        user_auth = request.user.id
        if form.is_valid():
            selected_date = form.cleaned_data['Return_date']
        if user_auth:
            user = User.objects.get(id=request.user.id)
            #borrowed_books_count = BorrowedBook.objects.filter(user=user).count()
            if selected_date-date.today() < timedelta(days=0):
                messages.error(request, "You have can't travel in Time!",'danger')
            elif user.membership=='V' and selected_date-date.today() >= timedelta(days=14):
                messages.error(request, "You have can't keep a book more than 14 days.",'danger')
            elif user.membership=='N' and selected_date-date.today() >= timedelta(days=7):
                messages.error(request, "You have can't keep a book more than 7 days.",'danger')
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
                #return redirect('library:borrow')
                
            return redirect('library:home')
        else:
            messages.error(request, 'Pls Login', 'warning')
            return redirect('account:User_Login')
    

class HomePage(View):
    def get(self, request):
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        genre_id = request.GET.get('genre_id')
        born_city = request.GET.get('born_city')
        page_number = request.GET.get('page')

        books = Books.objects.all()
        paginator = Paginator(books, 10)
        template_page = paginator.get_page(page_number) #we send this to our template for pagination
        

        if born_city:
            books = books.filter(author__born_city=born_city)

        if min_price and max_price:
            books = books.filter(price__range=(min_price, max_price))

        if genre_id:
            books = books.filter(genre__id=genre_id)

        return render(request, 'main.html', {'books': books})

    
class Search(View):
    def get(self,request):
        search_input = request.GET.get('search_input')
        result = Books.objects.filter(Q(title__icontains=search_input) | Q(description__icontains=search_input))
        return render(request,'search_result.html',{'result':result})
    
    def post(self):
        pass


