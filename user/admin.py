from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'username', 'is_active', 'is_staff', 'last_login')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('email', 'username')
    ordering = ('email',)
