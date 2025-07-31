from django.urls import path
from . import views
from . import branch_order_views

app_name = 'orders'

urlpatterns = [
    # Web views
    path('', views.OrderListView.as_view(), name='order-list'),
    path('create/', views.OrderCreateView.as_view(), name='order-create'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('<int:pk>/edit/', views.OrderUpdateView.as_view(), name='order-edit'),
    path('templates/', views.OrderTemplateListView.as_view(), name='template-list'),
    
    # Şube sipariş yönetimi
    path('branch/', branch_order_views.branch_order_list, name='branch_order_list'),
    path('branch/create/', branch_order_views.simple_branch_order_create, name='branch_order_create'),
    path('branch/create/advanced/', branch_order_views.BranchOrderCreateView.as_view(), name='branch_order_create_advanced'),
    path('branch/<int:order_id>/', branch_order_views.branch_order_detail, name='branch_order_detail'),
    path('branch/<int:order_id>/update-status/', branch_order_views.update_order_status_ajax, name='update_order_status_ajax'),
    path('branch/create-ajax/', branch_order_views.create_branch_order_ajax, name='create_branch_order_ajax'),
    
    # Üretim sipariş yönetimi
    path('production/', branch_order_views.production_orders_view, name='production_orders'),
    path('print/<int:order_id>/', branch_order_views.print_production_order, name='print_production_order'),
    
    # API endpoints
    path('api/', views.OrderListAPIView.as_view(), name='api-order-list'),
    path('api/create/', views.OrderListAPIView.as_view(), name='api-order-create'),
    path('api/<int:pk>/', views.OrderDetailAPIView.as_view(), name='api-order-detail'),
    path('api/<int:order_id>/status/', views.update_order_status_api, name='api-order-status'),
    path('api/templates/<int:template_id>/create-order/', views.create_order_from_template_api, name='api-create-from-template'),
] 