from django.contrib import admin
from .models import Author, Genre, Condition, Location
from book.models import Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    list_display = ('description',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('address', 'city', 'state', 'zip_code')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'condition', 'location', 'owner', 'is_available')
    search_fields = ('title', 'owner__username')
    list_filter = ('is_available', 'genre', 'condition')
    raw_id_fields = ('author', 'owner')
