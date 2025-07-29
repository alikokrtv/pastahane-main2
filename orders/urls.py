from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Web views
    path('', views.OrderListView.as_view(), name='order-list'),
    path('create/', views.OrderCreateView.as_view(), name='order-create'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('<int:pk>/edit/', views.OrderUpdateView.as_view(), name='order-edit'),
    path('templates/', views.OrderTemplateListView.as_view(), name='template-list'),
    
    # API endpoints
    path('api/', views.OrderListAPIView.as_view(), name='api-order-list'),
    path('api/create/', views.OrderListAPIView.as_view(), name='api-order-create'),
    path('api/<int:pk>/', views.OrderDetailAPIView.as_view(), name='api-order-detail'),
    path('api/<int:order_id>/status/', views.update_order_status_api, name='api-order-status'),
    path('api/templates/<int:template_id>/create-order/', views.create_order_from_template_api, name='api-create-from-template'),
] 