from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    # Web views
    path('', views.InventoryListView.as_view(), name='inventory-list'),
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/create/', views.ProductCreateView.as_view(), name='product-create'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('recipes/', views.RecipeListView.as_view(), name='recipe-list'),
    path('recipes/create/', views.RecipeCreateView.as_view(), name='recipe-create'),
    path('stock-movements/', views.StockMovementListView.as_view(), name='stock-movement-list'),
    path('waste/', views.WasteRecordListView.as_view(), name='waste-list'),
    
    # API endpoints
    path('api/', views.InventoryListAPIView.as_view(), name='api-inventory-list'),
    path('api/products/', views.ProductListAPIView.as_view(), name='api-product-list'),
    path('api/products/<int:pk>/', views.ProductDetailAPIView.as_view(), name='api-product-detail'),
    path('api/stock-movements/', views.StockMovementListAPIView.as_view(), name='api-stock-movement-list'),
    path('api/stock-movements/create/', views.StockMovementCreateAPIView.as_view(), name='api-stock-movement-create'),
    path('api/waste/', views.WasteRecordListAPIView.as_view(), name='api-waste-list'),
    path('api/waste/create/', views.WasteRecordCreateAPIView.as_view(), name='api-waste-create'),
] 