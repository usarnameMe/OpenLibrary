from django.contrib import admin
from .models import BookRequest


@admin.register(BookRequest)
class BookRequestAdmin(admin.ModelAdmin):
    list_display = ('book', 'borrower', 'owner', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('book__title', 'borrower__username', 'owner__username')
