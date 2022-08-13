from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, EmailConfirmToken, Contact


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = [
        'email',
        'is_staff',
        'user_type',
        'is_superuser',
        'is_active'
    ]

    list_editable = [
        'user_type',
        'is_staff',
        'is_superuser',
        'is_active',
    ]

    ordering = [
        'email',
    ]

    fieldsets = None

    fields = [
        'date_joined',
        'email',
        'password',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
        'is_superuser',
        'user_type',
        'last_login',
    ]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass


@admin.register(EmailConfirmToken)
class EmailConfirmTokenAdmin(admin.ModelAdmin):
    pass
