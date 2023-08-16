from django.urls import path
from . import views

app_name = 'library'
urlpatterns = [
    path('books/<int:books_id>/',views.BorrowBook.as_view(), name='borrow'),
    path('<int:borrowed_book_id>/',views.ReturnBook , name='return'),
    path('users/<int:user_id>/',views.UserProfile.as_view(), name='user'),
    path('',views.HomePage.as_view(), name='home'),

]