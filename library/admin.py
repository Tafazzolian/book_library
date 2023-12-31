from django.contrib import admin
from .models import Books, BorrowedBook, User, Author, Genre, Transaction
from account.models import OtpBanStatus,ErrorList

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
        list_display = ('full_name','email','phone','membership','expiration_date','wallet')
        search_fields = ('full_name','membership','email','phone')
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

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
        list_display = ('user','book','spent_amount','date')
        search_fields = ('user',)
        pass

@admin.register(OtpBanStatus)
class OtpBanStatusAdmin(admin.ModelAdmin):
        list_display = ('sms_function','blocked_time','ban_statuse')
        search_fields = ('sms_function',)
        pass

@admin.register(ErrorList)
class ErrorListAdmin(admin.ModelAdmin):
        list_display = ('error_list',)
        pass
