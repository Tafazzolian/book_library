from django.contrib import admin
from .models import Books, BorrowedBook

@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
        list_display = ('title','copies_available')
        search_fields = ('title',)
        pass
#admin.site.register(Books, BooksAdmin)

@admin.register(BorrowedBook)
class BorrowedBookAdmin(admin.ModelAdmin):
        list_display = ('user','book','borrow_date','return_date')
        search_fields = ('book','user','borrow_date')
        list_filter = ('user','book')
        raw_id_fields = ('user',)
        pass
#admin.site.register(BorrowedBook, BorrowedBookAdmin)

#admin.site.register(Relation)