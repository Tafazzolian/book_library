from django.contrib import admin
from .models import Books, BorrowedBook, User, Author, Genre

admin.site.register(Author)
admin.site.register(Genre) 


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
        list_display = ('full_name','email','phone','membership','expiration_date')
        search_fields = ('full_name','membership')
        list_filter = ('membership','expiration_date')
        pass
        

@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
        list_display = ('title','copies_available','author','description','genre','price','shabak')
        search_fields = ('title','price','shabak')
        pass


@admin.register(BorrowedBook)
class BorrowedBookAdmin(admin.ModelAdmin):
        list_display = ('user','book','borrow_date','return_date')
        search_fields = ('book','user','borrow_date')
        list_filter = ('user','book')
        raw_id_fields = ('user',)
        pass
