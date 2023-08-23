from django.contrib import admin
from .models import Books, BorrowedBook, User, Author, Genre

admin.site.site_header = 'Tank book library'
admin.site.index_title = 'Admin Panel'

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
        list_display = ('author','born_city','id')
        pass

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
        list_display = ('genre','id')
        pass


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
