from django.contrib import admin
from .models import Order, OrderItem, OrderStatusHistory, DeliveryRoute, Delivery


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'branch', 'customer_name', 'status', 'priority', 'requested_delivery_date', 'total_amount', 'created_at']
    list_filter = ['status', 'priority', 'branch', 'created_at']
    search_fields = ['order_number', 'customer_name', 'customer_phone']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    raw_id_fields = ['created_by', 'assigned_to']
    
    fieldsets = (
        ('📋 Temel Bilgiler', {
            'fields': ('order_number', 'branch', 'customer_name', 'customer_phone')
        }),
        ('📅 Tarihler', {
            'fields': ('requested_delivery_date', 'actual_delivery_date', 'created_at', 'updated_at')
        }),
        ('📊 Durum', {
            'fields': ('status', 'priority')
        }),
        ('💰 Fiyat Bilgileri', {
            'fields': ('subtotal', 'discount_amount', 'tax_amount', 'total_amount')
        }),
        ('👥 Atama', {
            'fields': ('created_by', 'assigned_to')
        }),
        ('📝 Notlar', {
            'fields': ('notes', 'internal_notes')
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'unit_price', 'get_total_price']
    list_filter = ['order__status', 'product__category']
    search_fields = ['order__order_number', 'product__name']
    raw_id_fields = ['order', 'product']
    
    def get_total_price(self, obj):
        return f"₺{obj.get_total_price():.2f}"
    get_total_price.short_description = 'Toplam'


@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ['order', 'from_status', 'to_status', 'changed_by', 'changed_at']
    list_filter = ['from_status', 'to_status', 'changed_at']
    search_fields = ['order__order_number', 'notes']
    readonly_fields = ['changed_at']
    raw_id_fields = ['order', 'changed_by']


@admin.register(DeliveryRoute)
class DeliveryRouteAdmin(admin.ModelAdmin):
    list_display = ['name', 'estimated_duration', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'delivery_areas']


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['order', 'route', 'driver', 'status', 'planned_start_time', 'actual_end_time']
    list_filter = ['status', 'route', 'planned_start_time']
    search_fields = ['order__order_number', 'driver__username', 'delivery_contact']
    raw_id_fields = ['order', 'route', 'driver']
    
    fieldsets = (
        ('📦 Sipariş Bilgileri', {
            'fields': ('order', 'route', 'driver', 'status')
        }),
        ('📍 Teslimat Adresi', {
            'fields': ('delivery_address', 'delivery_phone', 'delivery_contact')
        }),
        ('⏰ Zaman Planlaması', {
            'fields': ('planned_start_time', 'actual_start_time', 'planned_end_time', 'actual_end_time')
        }),
        ('📝 Ek Bilgiler', {
            'fields': ('delivery_notes', 'customer_signature', 'delivery_photo')
        }),
        ('📅 Kayıt Bilgileri', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']
