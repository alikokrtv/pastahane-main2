from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    # Web views
    path('', views.ReportListView.as_view(), name='report-list'),
    path('dashboard/', views.DashboardReportView.as_view(), name='dashboard-report'),
    path('inventory/', views.InventoryReportView.as_view(), name='inventory-report'),
    path('production/', views.ProductionReportView.as_view(), name='production-report'),
    path('sales/', views.SalesReportView.as_view(), name='sales-report'),
    
    # API endpoints
    path('dashboard/', views.DashboardDataAPIView.as_view(), name='api-dashboard-data'),
    path('activities/', views.ActivityReportAPIView.as_view(), name='api-activities'),
    path('inventory/', views.InventoryReportAPIView.as_view(), name='api-inventory-report'),
    path('production/', views.ProductionReportAPIView.as_view(), name='api-production-report'),
    path('sales/', views.SalesReportAPIView.as_view(), name='api-sales-report'),
    path('api/', views.ReportListAPIView.as_view(), name='api-report-list'),
] 