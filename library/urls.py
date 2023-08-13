from django.urls import path
from . import views

app_name = 'library'
urlpatterns = [
    path('books/<int:books_id>/',views.BorrowBook.as_view(), name='borrow'),
    path('',views.HomePage.as_view(), name='home'),

]