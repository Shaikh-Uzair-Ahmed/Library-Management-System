from django.contrib import admin
from .models import LibraryUser, BookMain, AvailBooks, UserBorrowed, LateFees, Request, Rating
# Register your models here.
from django.contrib import admin


class LibraryUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'lib_num', 'is_active')
    search_fields = ('user__username', 'lib_num')
    list_filter = ('is_active',)
    ordering = ('user',)

    # Optional: You can specify actions, or fields to show/edit in the admin
    fieldsets = (
        (None, {
            'fields': ('user', 'lib_num', 'is_active')
        }),
    )
    readonly_fields = ('lib_num',)

# Register models in the admin
admin.site.register(LibraryUser, LibraryUserAdmin)


class BookMainAdmin(admin.ModelAdmin):
    list_display = ('isbn', 'title', 'author', 'genre', 'cover_image')
    search_fields = ('isbn', 'title', 'author')
    ordering = ('title',)

admin.site.register(BookMain, BookMainAdmin)

class AvailBooksAdmin(admin.ModelAdmin):
    list_display = ('book', 'total_books', 'available_books', 'remaining_books')
    search_fields = ('book__title',)
    list_filter = ('book__genre',)

admin.site.register(AvailBooks, AvailBooksAdmin)

class UserBorrowedAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrow_date')
    search_fields = ('user__lib_num', 'book__title')
    list_filter = ('borrow_date',)


admin.site.register(UserBorrowed, UserBorrowedAdmin)


class LateFeesAdmin(admin.ModelAdmin):
    list_display = ('user_borrowed', 'days_late', 'fee')
    search_fields = ('user_borrowed__user__lib_num',)
    list_filter = ('days_late',)

admin.site.register(LateFees, LateFeesAdmin)

class RequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'isbn', 'title', 'request_date')
    search_fields = ('isbn', 'title', 'user__lib_num')
    list_filter = ('request_date',)


admin.site.register(Request, RequestAdmin)

class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'rating', 'review', 'created_at')
    search_fields = ('user__lib_num', 'book__title')
    list_filter = ('rating', 'created_at')

admin.site.register(Rating, RatingAdmin)
