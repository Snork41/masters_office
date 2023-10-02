from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (
                'Дополнительные поля',
                {
                    'fields': ('position',)}))
    fieldsets = (
        *UserAdmin.fieldsets,
        (
                'Дополнительные поля',
                {
                    'fields': ('position',)}))
