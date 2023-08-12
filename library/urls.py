from django.urls import path
from . import views

app_name = 'library'
urlpatterns = [
    #path('library/',views.library.as_view(), name='library_view'),
    path('',views.HomePage.as_view(), name='home'),

]