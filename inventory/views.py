from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib import messages
from django.db.models import Q, Sum, F
from django.http import JsonResponse
from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    ProductCategory, Product, Recipe, RecipeIngredient, 
    Inventory, StockMovement, WasteRecord
)
from .serializers import (
    ProductCategorySerializer, ProductSerializer, RecipeSerializer,
    InventorySerializer, StockMovementSerializer, WasteRecordSerializer
)


class ProductListView(LoginRequiredMixin, ListView):
    """Ürün listesi view'ı"""
    model = Product
    template_name = 'inventory/product_list.html'
    context_object_name = 'products'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Product.objects.select_related('category').filter(is_active=True)
        
        # Arama filtresi
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(sku__icontains=search) |
                Q(barcode__icontains=search)
            )
        
        # Kategori filtresi
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        
        return queryset.order_by('name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.filter(is_active=True)
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Ürün detay view'ı"""
    model = Product
    template_name = 'inventory/product_detail.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        
        # Stok bilgileri (kullanıcının şubesine göre)
        branch = self.request.user.branch
        if branch:
            try:
                inventory = Inventory.objects.get(product=product, branch=branch)
                context['inventory'] = inventory
            except Inventory.DoesNotExist:
                context['inventory'] = None
        
        # Reçete bilgileri
        context['recipes'] = Recipe.objects.filter(
            recipeingredient__ingredient=product
        ).distinct()
        
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Ürün oluşturma view'ı"""
    model = Product
    template_name = 'inventory/product_create.html'
    fields = ['name', 'description', 'category', 'sku', 'barcode', 'unit', 
              'cost_price', 'selling_price', 'shelf_life_days', 'storage_conditions']


class RecipeListView(LoginRequiredMixin, ListView):
    """Reçete listesi view'ı"""
    model = Recipe
    template_name = 'inventory/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Recipe.objects.filter(is_active=True)
        
        # Arama filtresi
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )
        
        return queryset.order_by('name')


class RecipeDetailView(LoginRequiredMixin, DetailView):
    """Reçete detay view'ı"""
    model = Recipe
    template_name = 'inventory/recipe_detail.html'
    context_object_name = 'recipe'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.get_object()
        
        # Reçete malzemeleri
        context['ingredients'] = RecipeIngredient.objects.filter(
            recipe=recipe
        ).select_related('ingredient')
        
        return context


class RecipeCreateView(LoginRequiredMixin, CreateView):
    """Reçete oluşturma view'ı"""
    model = Recipe
    template_name = 'inventory/recipe_create.html'
    fields = ['name', 'description', 'instructions', 'preparation_time',
              'cooking_time', 'yield_quantity', 'yield_unit', 'difficulty_level']


class InventoryListView(LoginRequiredMixin, ListView):
    """Stok listesi view'ı"""
    model = Inventory
    template_name = 'inventory/inventory_list.html'
    context_object_name = 'inventories'
    paginate_by = 20
    
    def get_queryset(self):
        # Kullanıcının şubesindeki stokları göster
        branch = self.request.user.branch
        queryset = Inventory.objects.select_related(
            'product', 'product__category', 'branch'
        ).filter(branch=branch)
        
        # Düşük stok uyarısı filtresi
        low_stock = self.request.GET.get('low_stock')
        if low_stock:
            queryset = queryset.filter(quantity__lte=F('minimum_stock'))
        
        # Arama filtresi
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(product__name__icontains=search) |
                Q(product__sku__icontains=search)
            )
        
        return queryset.order_by('product__name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        branch = self.request.user.branch
        
        # Dashboard statistikleri
        if branch:
            inventories = Inventory.objects.filter(branch=branch)
            context.update({
                'total_products': inventories.count(),
                'low_stock_count': inventories.filter(
                    current_stock__lte=F('min_stock_level')
                ).count(),
                'out_of_stock_count': inventories.filter(current_stock=0).count(),
            })
        
        return context


class StockMovementListView(LoginRequiredMixin, ListView):
    """Stok hareket listesi view'ı"""
    model = StockMovement
    template_name = 'inventory/stock_movement_list.html'
    context_object_name = 'movements'
    paginate_by = 20
    
    def get_queryset(self):
        # Kullanıcının şubesindeki hareketleri göster - inventory üzerinden filtrele
        branch = self.request.user.branch
        if branch:
            queryset = StockMovement.objects.select_related(
                'inventory__product', 'inventory__branch', 'created_by'
            ).filter(inventory__branch=branch)
        else:
            queryset = StockMovement.objects.select_related(
                'inventory__product', 'inventory__branch', 'created_by'
            ).all()
        
        # Hareket tipi filtresi
        movement_type = self.request.GET.get('movement_type')
        if movement_type:
            queryset = queryset.filter(movement_type=movement_type)
        
        # Arama filtresi
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(inventory__product__name__icontains=search) |
                Q(inventory__product__sku__icontains=search) |
                Q(reference_number__icontains=search)
            )
        
        return queryset.order_by('-created_at')


class WasteRecordListView(LoginRequiredMixin, ListView):
    """Fire kayıt listesi view'ı"""
    model = WasteRecord
    template_name = 'inventory/waste_list.html'
    context_object_name = 'waste_records'
    paginate_by = 20
    
    def get_queryset(self):
        # Kullanıcının şubesindeki fire kayıtlarını göster
        branch = self.request.user.branch
        if branch:
            return WasteRecord.objects.select_related(
                'inventory__product', 'inventory__branch', 'recorded_by'
            ).filter(inventory__branch=branch).order_by('-waste_date')
        else:
            return WasteRecord.objects.select_related(
                'inventory__product', 'inventory__branch', 'recorded_by'
            ).all().order_by('-waste_date')


# API Views
class ProductListAPIView(generics.ListAPIView):
    """API Ürün listesi"""
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'sku', 'barcode']
    filterset_fields = ['category', 'is_active']
    
    def get_queryset(self):
        return Product.objects.select_related('category').filter(is_active=True)


class ProductDetailAPIView(generics.RetrieveAPIView):
    """API Ürün detay"""
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.select_related('category')


class InventoryListAPIView(generics.ListAPIView):
    """API Stok listesi"""
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['product__name', 'product__sku']
    
    def get_queryset(self):
        # Kullanıcının şubesindeki stokları döndür
        branch = self.request.user.branch
        return Inventory.objects.select_related(
            'product', 'branch'
        ).filter(branch=branch)


class StockMovementListAPIView(generics.ListAPIView):
    """API Stok hareket listesi"""
    serializer_class = StockMovementSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Kullanıcının şubesindeki hareketleri döndür
        branch = self.request.user.branch
        if branch:
            return StockMovement.objects.filter(inventory__branch=branch)
        else:
            return StockMovement.objects.all()


class StockMovementCreateAPIView(generics.CreateAPIView):
    """API Stok hareket oluşturma"""
    serializer_class = StockMovementSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        # Hareketi oluşturan kullanıcı ve şube bilgilerini ekle
        serializer.save(
            created_by=self.request.user,
            branch=self.request.user.branch
        )


class WasteRecordListAPIView(generics.ListAPIView):
    """API Fire kayıt listesi"""
    serializer_class = WasteRecordSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Kullanıcının şubesindeki fire kayıtlarını döndür
        branch = self.request.user.branch
        if branch:
            return WasteRecord.objects.filter(inventory__branch=branch)
        else:
            return WasteRecord.objects.all()


class WasteRecordCreateAPIView(generics.CreateAPIView):
    """API Fire kayıt oluşturma"""
    serializer_class = WasteRecordSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(
            recorded_by=self.request.user,
            branch=self.request.user.branch
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def low_stock_alert_api(request):
    """Düşük stok uyarı API'si"""
    branch = request.user.branch
    if not branch:
        return Response({'error': 'Şube bilgisi bulunamadı'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    low_stock_items = Inventory.objects.select_related('product').filter(
        branch=branch,
        quantity__lte=F('minimum_stock')
    )
    
    data = []
    for item in low_stock_items:
        data.append({
            'product_name': item.product.name,
            'current_stock': item.quantity,
            'min_stock_level': item.minimum_stock,
            'unit': item.product.unit,
        })
    
    return Response({
        'count': len(data),
        'items': data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def record_waste_api(request):
    """Fire kayıt API'si"""
    serializer = WasteRecordSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(
            recorded_by=request.user,
            branch=request.user.branch
        )
        return Response({
            'status': 'success',
            'message': 'Fire kaydı başarıyla oluşturuldu',
            'data': serializer.data
        })
    
    return Response({
        'status': 'error',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
