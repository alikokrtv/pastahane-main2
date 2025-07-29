from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Branch, UserProfile


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'branch_type', 'phone', 'is_active', 'created_at']
    list_filter = ['branch_type', 'is_active', 'created_at']
    search_fields = ['name', 'address', 'phone']
    ordering = ['name']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (_('Temel Bilgiler'), {
            'fields': ('name', 'branch_type', 'is_active')
        }),
        (_('İletişim Bilgileri'), {
            'fields': ('address', 'phone', 'email')
        }),
        (_('Zaman Bilgileri'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (_('Ek Bilgiler'), {
            'fields': ('role', 'branch', 'phone', 'employee_id', 'is_active_employee', 'hire_date')
        }),
        (_('Zaman Bilgileri'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = UserAdmin.readonly_fields + ('created_at', 'updated_at')
    
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'branch', 'is_active', 'is_active_employee']
    list_filter = UserAdmin.list_filter + ('role', 'branch', 'is_active_employee', 'hire_date')
    search_fields = UserAdmin.search_fields + ('employee_id', 'phone')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('branch')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'birth_date', 'emergency_contact', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'emergency_contact']
    raw_id_fields = ['user']
    
    fieldsets = (
        (_('Kullanıcı'), {
            'fields': ('user',)
        }),
        (_('Kişisel Bilgiler'), {
            'fields': ('avatar', 'birth_date', 'address')
        }),
        (_('Acil Durum İletişim'), {
            'fields': ('emergency_contact', 'emergency_phone')
        }),
        (_('Notlar'), {
            'fields': ('notes',)
        }),
        (_('Zaman Bilgileri'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']
