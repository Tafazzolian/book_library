from django.db import models
from account.models import CustomUser as User

class Books(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=6 , decimal_places=2, default=0.00)
    shabak = models.CharField(max_length=150,null=True)
    copies_available = models.PositiveIntegerField(default=4)
    genre = models.ForeignKey('Genre', on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title
    
class Genre(models.Model):
    genre = models.CharField(max_length=50,null=True)

    def __str__(self):
        return self.genre

class Author(models.Model):
    author = models.CharField(max_length=150,null=True)
    born_city = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.author

    
class BorrowedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    borrow_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.full_name} borrowed {self.book.title}"