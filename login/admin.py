from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, cars


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'phone_number', 'user_type', 'is_verified', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_verified', 'is_staff', 'is_active')
    search_fields = ('email', 'name', 'phone_number')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username', 'name', 'phone_number', 'age', 'profile_picture')}),
        ('Permissions', {'fields': ('user_type', 'is_staff', 'is_active', 'is_verified', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'user_type', 'is_staff', 'is_active'),
        }),
    )


@admin.register(cars)
class CarsAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'owner', 'is_approved', 'chassis_number', 'license_plate_number')
    search_fields = ('make', 'model', 'chassis_number', 'license_plate_number')
    list_filter = ('is_approved', 'fuel_type')
