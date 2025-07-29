from rest_framework import serializers
from .models import (
    Order, OrderItem, OrderStatusHistory, DeliveryRoute,
    Delivery, OrderTemplate, OrderTemplateItem
)


class OrderItemSerializer(serializers.ModelSerializer):
    """Sipariş kalemi serializer'ı"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_unit = serializers.CharField(source='product.unit', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'order', 'product', 'product_name', 'product_unit',
            'quantity', 'unit_price', 'discount_amount', 'total_price',
            'notes'
        ]
        read_only_fields = ['id']


class OrderStatusHistorySerializer(serializers.ModelSerializer):
    """Sipariş durum geçmişi serializer'ı"""
    changed_by_name = serializers.CharField(source='changed_by.get_full_name', read_only=True)
    
    class Meta:
        model = OrderStatusHistory
        fields = [
            'id', 'order', 'old_status', 'new_status', 'changed_by',
            'changed_by_name', 'changed_at', 'notes'
        ]
        read_only_fields = ['id', 'changed_by', 'changed_at']


class OrderSerializer(serializers.ModelSerializer):
    """Sipariş serializer'ı"""
    customer_branch_name = serializers.CharField(source='customer_branch.name', read_only=True)
    delivery_branch_name = serializers.CharField(source='delivery_branch.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    items = OrderItemSerializer(many=True, read_only=True, source='orderitem_set')
    status_history = OrderStatusHistorySerializer(many=True, read_only=True, source='orderstatushistory_set')
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'customer_name', 'customer_phone', 
            'customer_email', 'customer_branch', 'customer_branch_name',
            'delivery_branch', 'delivery_branch_name', 'delivery_address',
            'delivery_date', 'status', 'priority', 'subtotal', 'tax_amount',
            'discount_amount', 'total_amount', 'special_instructions',
            'created_by', 'created_by_name', 'created_at', 'updated_at',
            'items', 'status_history'
        ]
        read_only_fields = [
            'id', 'order_number', 'created_by', 'created_at', 'updated_at',
            'subtotal', 'tax_amount', 'total_amount'
        ]


class DeliveryRouteSerializer(serializers.ModelSerializer):
    """Teslimat rotası serializer'ı"""
    
    class Meta:
        model = DeliveryRoute
        fields = [
            'id', 'name', 'description', 'estimated_duration',
            'max_capacity', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class DeliverySerializer(serializers.ModelSerializer):
    """Teslimat serializer'ı"""
    order_number = serializers.CharField(source='order.order_number', read_only=True)
    customer_name = serializers.CharField(source='order.customer_name', read_only=True)
    driver_name = serializers.CharField(source='driver.get_full_name', read_only=True)
    route_name = serializers.CharField(source='route.name', read_only=True)
    
    class Meta:
        model = Delivery
        fields = [
            'id', 'order', 'order_number', 'customer_name', 'driver',
            'driver_name', 'route', 'route_name', 'delivery_date',
            'delivery_time_start', 'delivery_time_end', 'status',
            'actual_delivery_time', 'delivery_notes', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class OrderTemplateItemSerializer(serializers.ModelSerializer):
    """Sipariş şablonu kalemi serializer'ı"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_unit = serializers.CharField(source='product.unit', read_only=True)
    
    class Meta:
        model = OrderTemplateItem
        fields = [
            'id', 'template', 'product', 'product_name', 'product_unit',
            'quantity', 'notes'
        ]
        read_only_fields = ['id']


class OrderTemplateSerializer(serializers.ModelSerializer):
    """Sipariş şablonu serializer'ı"""
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    items = OrderTemplateItemSerializer(many=True, read_only=True, source='ordertemplateitem_set')
    
    class Meta:
        model = OrderTemplate
        fields = [
            'id', 'name', 'description', 'branch', 'branch_name',
            'is_active', 'created_by', 'created_by_name', 'created_at',
            'updated_at', 'items'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at'] 