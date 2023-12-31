from django.views import View
from .models import Books,BorrowedBook, Transaction
from account.models import CustomUser as User
from datetime import date, timedelta
from django.shortcuts import get_object_or_404,render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import DateInputForm, BooksCrudForm, WalletChargeForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BookSerializer
from .repository import Model
from django.core.paginator import Paginator
from django.http import JsonResponse


class UserProfile(LoginRequiredMixin,View):
    template_class = 'library/user_profile.html'
    form_template = WalletChargeForm

    def dispatch(self, request, user_id):
        if user_id != request.user.id:
            messages.error(request, 'No cheating!', 'danger')
            return redirect('library:home')
        return super().dispatch(request, user_id)


    def get(self,request, user_id):
        user = Model.get(model=User,id=user_id)
        borrowed_books = Model.filter(BorrowedBook,user = user.id)
        return render(request,self.template_class,{'borrowed_books': borrowed_books,'user':user,'form':self.form_template})
    
    def post(self,request, user_id):
        user = Model.get(model=User,id=user_id)
        form = self.form_template(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            user.wallet += amount
            Model.save(user)
            messages.success(request,'You got rich!')
        return redirect('library:user',user_id=user_id)


class ReturnBook(LoginRequiredMixin,View):
    template_class = 'library/user_profile.html'
    
    def dispatch(self, request,borrowed_book_id):
        borrow_id = Model.get(model=BorrowedBook,id=borrowed_book_id)#get_object_or_404(BorrowedBook, id=borrowed_book_id)
        if borrow_id.user.id != request.user.id:
            messages.error(request, 'No cheating!', 'danger')
            return redirect('library:home')
        return super().dispatch(request, borrowed_book_id)
    
    def get(self, request, borrowed_book_id):
        borrowed_book = Model.get(model=BorrowedBook,id=borrowed_book_id)#get_object_or_404(BorrowedBook, id=borrowed_book_id)
        book = borrowed_book.book
        book.copies_available += 1
        Model.save(book)
        Model.delete(borrowed_book)
        messages.success(request, "You have successfully returned the book.")
        return redirect('library:home')


class BorrowBook(View):
    form_class = DateInputForm
    template_class = 'library/borrow.html'
    
    def get(self,request, books_id):
        book = Model.get(model=Books, id=books_id)#get_object_or_404(Books, id=books_id)
        form = self.form_class()
        return render(request,self.template_class,{'form':form,'book':book})
    
    def post(self,request, books_id):
        form = self.form_class(request.POST)    
        book = Model.get(model=Books, id=books_id)
        user_auth = request.user.id
        if form.is_valid():
            selected_date = form.cleaned_data['Return_date']
        if user_auth:
            user = Model.get(model=User,id=request.user.id)
            user_credit = int(user.wallet)
            book_price = int(book.price)
            if user_credit-book_price < 0 :
                messages.error(request, "Not enough money!",'danger')

            elif selected_date-date.today() < timedelta(days=0):
                messages.error(request, "You have can't travel in Time!",'danger')

            elif user.membership=='V' and selected_date-date.today() >= timedelta(days=14):
                messages.error(request, "VIP users can borrow a book for max 14 days.",'danger')

            elif user.membership=='N' and selected_date-date.today() >= timedelta(days=7):
                messages.error(request, "NORMAL users can borrow a book for max 7 days.",'danger')

            elif book.copies_available <= 0:
                messages.error(request, "No copies of this book are currently available!",'danger')

            elif form.is_valid():
                #race condition check
                try: 
                    book.copies_available -= 1
                    Model.save(book)
                    borrowed_book = BorrowedBook(user=user, book=book, borrow_date=date.today(), return_date=selected_date)
                    Model.save(borrowed_book)
                    user.wallet = user_credit-book_price
                    Model.save(user)
                    transaction = Transaction(user=user, book=book, spent_amount=book_price, date=date.today())
                    Model.save(transaction)
                    messages.success(request, f"You have successfully borrowed '{book.title}'.")
                except:
                    messages.error(request, "Someone else borrowed the last copy of this book just before you!")
            else:
                self.form_class()                
            return redirect('library:home')
        else:
            messages.error(request, 'Pls Login', 'warning')
            return redirect('account:User_Login')
    
class Subscription(View):
    def get(self,request):
        try:
            user = Model.get(model=User, id=request.user.id) #User.objects.get(id=request.user.id)
            return render(request, 'library/sub.html',{'user_id':user.id})
        except:
            user = 0
            return render(request, 'library/sub.html',{'user_id':user})

class Buy(View):
    def get(self,request, user_id):
        try:
            user = Model.get(model=User, id=user_id)#User.objects.get(id=user_id)
            if user.membership == 'V':
                messages.warning(request, 'You are already a VIP member!')
                return redirect('library:home')
            elif user.wallet < 200:
                messages.warning(request, 'You dont have enough money in your wallet!')
                return redirect('library:home')
            else:
                user.membership = 'V' #User(id=user,membership='V')
                user.expiration_date = date.today()+timedelta(days=31)
                user.wallet -= 200
                Model.save(user)
                messages.success(request,'You are now a VIP member')
                return redirect('library:home')
        except:
            messages.error(request, 'Pls Login first', 'warning')
            return redirect('account:User_Login')


class HomePage(View):
    def get(self, request):
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        genre_id = request.GET.get('genre_id')
        born_city = request.GET.get('born_city')
        Price = request.GET.get('price')
        
        #Pagination
        #page_number = request.GET.get('page')
        #paginator = Paginator(books, 10)
        #template_page = paginator.get_page(page_number)
        books = Books.objects.values('title','genre__genre','author','price','id','copies_available')
        
        if born_city:
            books = books.filter(author__born_city=born_city)

        if min_price and max_price:
            books = books.filter(price__range=(min_price, max_price))

        if Price:
            books = books.order_by(Price)

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

class BooksCrud(View):
    form_class = BooksCrudForm
    template_class = 'library/bcrud.html'

    def get(self,request,book_id):
        books = Books.objects.values('id','title')
        if book_id == 0:
            form = self.form_class
            return render(request,self.template_class,{'form':form,'books':books})
        else:
            instance = get_object_or_404(Books, pk=book_id)
            form = self.form_class(instance=instance)
            return render(request,self.template_class,{'form':form,'books':books})

        
    def post(self,request,book_id):
        form = self.form_class(request.POST)
        if book_id == 0 and form.is_valid():
            form.save()
            messages.success(request, 'New Book Added successfuly')
            return redirect('library:home')
        elif book_id != 0:
            instance = get_object_or_404(Books, pk=book_id)
            form = self.form_class(request.POST, instance=instance)
            updated_book = form.save(commit=False)
            #any additional fields that were missing in the form must be filled here
            updated_book.save()
            messages.success(request,'update success','success')
            return redirect('library:home')

class BookDelete(View):
    @method_decorator(login_required)
    def get(self,request,book_id):
        if request.user.is_admin :
            book = get_object_or_404(Books, id=book_id)
            book.delete()
            messages.warning(request, f'{book.title} deleted!','danger')
        else:
            messages.warning(request,'You are not an Admin!')
        return redirect('library:home')        



class BookList(APIView):

    def get(self,request):
        books = Books.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            min_price = request.data.get('min_price')
            max_price = request.data.get('max_price')
            genre_id = request.data.get('genre_id')
            born_city = request.data.get('born_city')
            price = request.data.get('price')

            books = Books.objects.all()
            if born_city:
                books = books.filter(author__born_city=born_city)

            if min_price and max_price:
                books = books.filter(price__range=(min_price, max_price))

            if price:
                books = books.order_by(price)

            if genre_id:
                books = books.filter(genre__id=genre_id)

            serializer = BookSerializer(books, many=True)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)