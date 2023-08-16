from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    MEMBERSHIP_NORMAL = 'N'
    MEMBERSHIP_VIP = 'V'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_NORMAL,'Normal'),
        (MEMBERSHIP_VIP,'VIP'),
    ]
    first_name = models.CharField(max_length=255,null=True)
    last_name = models.CharField(max_length=255,null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255,null=True)
    expiration_date = models.DateField(null=True)
    #choice field
    membership = models.CharField(max_length=1, choices= MEMBERSHIP_CHOICES, default= MEMBERSHIP_NORMAL)

class Genre(models.Model):
    genre = models.CharField(max_length=50)
    featured_books = models.ForeignKey(
        'Books', on_delete=models.SET_NULL, null=True, related_name='genre')


class Author(models.Model):
    author = models.CharField(max_length=150)
    featured_books = models.ForeignKey(
        'Books', on_delete=models.SET_NULL, null=True, related_name='author')

class Books(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6 , decimal_places=2)
    shabak = models.CharField(max_length=150)
    copies_available = models.PositiveIntegerField(default=4)

    def __str__(self):
        return self.title

class BorrowedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    borrow_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"