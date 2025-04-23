from django.contrib import admin
from .models import Author, Book, Review, Publisher, Store


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    search_fields = ('title', 'author__name')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'bio')
    search_fields = ('name', 'bio')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("book")


admin.site.register(Publisher)
admin.site.register(Store)
