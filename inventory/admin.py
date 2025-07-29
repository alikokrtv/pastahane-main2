from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from .models import (
    ProductCategory, Product, Recipe, RecipeIngredient,
    Inventory, StockMovement, WasteRecord
)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'product_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']
    date_hierarchy = 'created_at'
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = _('Ürün Sayısı')


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    autocomplete_fields = ['ingredient']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'product', 'yield_quantity', 'total_time', 'is_active', 'created_by']
    list_filter = ['is_active', 'created_at', 'product__category']
    search_fields = ['name', 'product__name', 'description']
    autocomplete_fields = ['product', 'created_by']
    inlines = [RecipeIngredientInline]
    
    fieldsets = (
        (_('Temel Bilgiler'), {
            'fields': ('product', 'name', 'description', 'is_active')
        }),
        (_('Miktar ve Süre'), {
            'fields': ('yield_quantity', 'preparation_time', 'cooking_time')
        }),
        (_('Talimatlar'), {
            'fields': ('instructions',)
        }),
        (_('Kayıt Bilgileri'), {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']
    
    def total_time(self, obj):
        return f"{obj.preparation_time + obj.cooking_time} dk"
    total_time.short_description = _('Toplam Süre')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'sku', 'unit', 'price_per_unit', 'cost_per_unit', 'profit_margin', 'is_active', 'is_produced']
    list_filter = ['category', 'unit', 'is_active', 'is_produced', 'created_at']
    search_fields = ['name', 'sku', 'barcode', 'description']
    autocomplete_fields = ['category']
    ordering = ['name']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (_('Temel Bilgiler'), {
            'fields': ('name', 'category', 'description', 'is_active')
        }),
        (_('Stok Bilgileri'), {
            'fields': ('sku', 'barcode', 'unit', 'is_produced', 'shelf_life_days')
        }),
        (_('Fiyat Bilgileri'), {
            'fields': ('price_per_unit', 'cost_per_unit')
        }),
        (_('Zaman Bilgileri'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']
    
    def profit_margin(self, obj):
        margin = obj.get_profit_margin()
        color = 'green' if margin > 20 else 'orange' if margin > 10 else 'red'
        return format_html(
            '<span style="color: {};">{:.1f}%</span>',
            color, margin
        )
    profit_margin.short_description = _('Kar Marjı')


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['branch', 'product', 'quantity', 'reserved_quantity', 'available_quantity', 'stock_status', 'last_updated']
    list_filter = ['branch', 'product__category', 'last_updated']
    search_fields = ['branch__name', 'product__name', 'product__sku']
    autocomplete_fields = ['branch', 'product', 'last_updated_by']
    ordering = ['branch', 'product']
    date_hierarchy = 'last_updated'
    
    fieldsets = (
        (_('Lokasyon ve Ürün'), {
            'fields': ('branch', 'product')
        }),
        (_('Stok Miktarları'), {
            'fields': ('quantity', 'reserved_quantity', 'minimum_stock', 'maximum_stock')
        }),
        (_('Güncelleme Bilgileri'), {
            'fields': ('last_updated_by', 'last_updated'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['last_updated']
    
    def available_quantity(self, obj):
        return obj.get_available_quantity()
    available_quantity.short_description = _('Kullanılabilir Miktar')
    
    def stock_status(self, obj):
        if obj.is_out_of_stock():
            return format_html('<span style="color: red;">Tükendi</span>')
        elif obj.is_low_stock():
            return format_html('<span style="color: orange;">Düşük</span>')
        else:
            return format_html('<span style="color: green;">Normal</span>')
    stock_status.short_description = _('Stok Durumu')


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['inventory', 'movement_type', 'quantity', 'reference_number', 'created_by', 'created_at']
    list_filter = ['movement_type', 'created_at', 'inventory__branch']
    search_fields = ['inventory__product__name', 'reference_number', 'notes']
    autocomplete_fields = ['inventory', 'created_by']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (_('Hareket Bilgileri'), {
            'fields': ('inventory', 'movement_type', 'quantity')
        }),
        (_('Referans ve Notlar'), {
            'fields': ('reference_number', 'notes')
        }),
        (_('Kayıt Bilgileri'), {
            'fields': ('created_by', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at']
    
    def has_change_permission(self, request, obj=None):
        # Stok hareketleri değiştirilemez
        return False


@admin.register(WasteRecord)
class WasteRecordAdmin(admin.ModelAdmin):
    list_display = ['inventory', 'quantity', 'reason', 'cost_impact', 'created_by', 'created_at']
    list_filter = ['reason', 'created_at', 'inventory__branch']
    search_fields = ['inventory__product__name', 'description']
    autocomplete_fields = ['inventory', 'created_by']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (_('İmha Bilgileri'), {
            'fields': ('inventory', 'quantity', 'reason')
        }),
        (_('Açıklama ve Maliyet'), {
            'fields': ('description', 'cost_impact')
        }),
        (_('Kayıt Bilgileri'), {
            'fields': ('created_by', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['cost_impact', 'created_at']
    
    def has_change_permission(self, request, obj=None):
        # İmha kayıtları değiştirilemez
        return False


# RecipeIngredient için ayrı admin (eğer doğrudan erişim istenirse)
@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'ingredient', 'quantity', 'unit', 'cost']
    list_filter = ['unit', 'created_at']
    search_fields = ['recipe__name', 'ingredient__name']
    autocomplete_fields = ['recipe', 'ingredient']
    ordering = ['recipe', 'ingredient']
    
    def cost(self, obj):
        return f"{obj.get_cost():.2f} TL"
    cost.short_description = _('Maliyet')
