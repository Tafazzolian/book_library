from django.urls import path
from . import views

app_name = 'library'
urlpatterns = [
    path('books/<int:books_id>/',views.borrow_book, name='borrow'),
    path('',views.HomePage.as_view(), name='home'),

]