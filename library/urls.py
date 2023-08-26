from django.urls import path
from . import views

app_name = 'library'
urlpatterns = [
    path('books/<int:books_id>/',views.BorrowBook.as_view(), name='borrow'),
    path('books-crud/<int:book_id>/',views.BooksCrud.as_view(), name='bcrud'),
    path('books-delete/<int:book_id>/',views.BookDelete.as_view(), name='bdelete'),
    path('Sub/',views.Subscription.as_view(), name='sub'),
    path('buy/<int:user_id>/',views.Buy.as_view(), name='buy'),
    path('return/<int:borrowed_book_id>/',views.ReturnBook.as_view() , name='return'),
    path('users/<int:user_id>/',views.UserProfile.as_view(), name='user'),
    path('search/',views.Search.as_view(), name='search'),
    path('api/book-list/',views.BookList.as_view(),name='bookapi'),
    path('',views.HomePage.as_view(), name='home'),

]