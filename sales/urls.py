from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    # Web views
    path('', views.SalesListView.as_view(), name='sales-list'),
    path('daily/', views.DailySalesView.as_view(), name='daily-sales'),
    path('reports/', views.SalesReportView.as_view(), name='sales-reports'),
    path('viapos/', views.ViaposSalesListView.as_view(), name='viapos-sales-list'),
    path('viapos/export/', views.ViaposSalesExportView.as_view(), name='viapos-sales-export'),
    
    # API endpoints
    path('api/', views.SalesListAPIView.as_view(), name='api-sales-list'),
    path('api/daily/', views.DailySalesAPIView.as_view(), name='api-daily-sales'),
    path('api/summary/', views.SalesSummaryAPIView.as_view(), name='api-sales-summary'),
] 