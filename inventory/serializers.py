from rest_framework import serializers
from .models import (
    ProductCategory, Product, Recipe, RecipeIngredient,
    Inventory, StockMovement, WasteRecord
)


class ProductCategorySerializer(serializers.ModelSerializer):
    """Ürün kategori serializer'ı"""
    
    class Meta:
        model = ProductCategory
        fields = [
            'id', 'name', 'description', 'parent', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):
    """Ürün serializer'ı"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'category', 'category_name',
            'sku', 'barcode', 'unit', 'cost_price', 'selling_price',
            'shelf_life_days', 'storage_conditions', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Reçete malzemesi serializer'ı"""
    ingredient_name = serializers.CharField(source='ingredient.name', read_only=True)
    ingredient_unit = serializers.CharField(source='ingredient.unit', read_only=True)
    
    class Meta:
        model = RecipeIngredient
        fields = [
            'id', 'recipe', 'ingredient', 'ingredient_name', 
            'ingredient_unit', 'quantity', 'notes'
        ]
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """Reçete serializer'ı"""
    ingredients = RecipeIngredientSerializer(many=True, read_only=True, source='recipeingredient_set')
    
    class Meta:
        model = Recipe
        fields = [
            'id', 'name', 'description', 'instructions', 'preparation_time',
            'cooking_time', 'yield_quantity', 'yield_unit', 'difficulty_level',
            'is_active', 'created_at', 'updated_at', 'ingredients'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class InventorySerializer(serializers.ModelSerializer):
    """Stok serializer'ı"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_unit = serializers.CharField(source='product.unit', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    stock_status = serializers.SerializerMethodField()
    
    class Meta:
        model = Inventory
        fields = [
            'id', 'product', 'product_name', 'product_unit', 'branch',
            'branch_name', 'current_stock', 'min_stock_level', 
            'max_stock_level', 'reorder_point', 'stock_status',
            'last_updated'
        ]
        read_only_fields = ['id', 'last_updated']
    
    def get_stock_status(self, obj):
        if obj.current_stock <= 0:
            return 'out_of_stock'
        elif obj.current_stock <= obj.min_stock_level:
            return 'low_stock'
        elif obj.current_stock >= obj.max_stock_level:
            return 'overstock'
        else:
            return 'normal'


class StockMovementSerializer(serializers.ModelSerializer):
    """Stok hareket serializer'ı"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = StockMovement
        fields = [
            'id', 'product', 'product_name', 'branch', 'branch_name',
            'movement_type', 'quantity', 'unit_cost', 'total_cost',
            'reference_number', 'notes', 'created_by', 'created_by_name',
            'created_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at']


class WasteRecordSerializer(serializers.ModelSerializer):
    """Fire kayıt serializer'ı"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    recorded_by_name = serializers.CharField(source='recorded_by.get_full_name', read_only=True)
    
    class Meta:
        model = WasteRecord
        fields = [
            'id', 'product', 'product_name', 'branch', 'branch_name',
            'quantity', 'waste_reason', 'waste_date', 'cost_impact',
            'notes', 'recorded_by', 'recorded_by_name', 'created_at'
        ]
        read_only_fields = ['id', 'recorded_by', 'created_at'] 