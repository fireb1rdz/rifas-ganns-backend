from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Address, Email, Phone, SocialMedia
from apps.configurations.models import UserConfiguration

class EmailInline(admin.TabularInline):
    model = Email
    extra = 1
class AddressInline(admin.TabularInline):
    model = Address
    extra = 1

class PhoneInline(admin.TabularInline):
    model = Phone
    extra = 1
    
class SocialMediaInline(admin.TabularInline):
    model = SocialMedia
    extra = 1
    
class UserConfigurationInline(admin.StackedInline):
    model = UserConfiguration
    extra = 1  
    min_num = 0
    max_num = 1 
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("username", "is_staff", "is_active", "cpf", "birth_date", "is_superuser", "is_verified", "profile_picture", "bio", "last_login")
    search_fields = ("username",)
    inlines = [EmailInline, AddressInline, PhoneInline, SocialMediaInline, UserConfigurationInline]
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("cpf", "birth_date", "is_verified", "profile_picture", "bio")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("cpf", "birth_date", "is_verified", "profile_picture", "bio")}),
    )
    

