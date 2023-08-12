from django.db import models
from django.contrib.auth.models import User

class Books(models.Model):
    title = models.CharField(max_length=100)
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