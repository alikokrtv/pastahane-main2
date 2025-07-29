from django.urls import path
from . import views

app_name = 'production'

urlpatterns = [
    # Web views
    path('', views.ProductionPlanListView.as_view(), name='plan-list'),
    path('plans/create/', views.ProductionPlanCreateView.as_view(), name='plan-create'),
    path('plans/<int:pk>/', views.ProductionPlanDetailView.as_view(), name='plan-detail'),
    path('batches/', views.ProductionBatchListView.as_view(), name='batch-list'),
    path('batches/create/', views.ProductionBatchCreateView.as_view(), name='batch-create'),
    path('batches/<int:pk>/', views.ProductionBatchDetailView.as_view(), name='batch-detail'),
    path('quality/', views.QualityCheckListView.as_view(), name='quality-list'),
    path('reports/', views.ProductionReportListView.as_view(), name='report-list'),
    
    # API endpoints
    path('api/plans/', views.ProductionPlanListAPIView.as_view(), name='api-plan-list'),
    path('api/plans/create/', views.ProductionPlanCreateAPIView.as_view(), name='api-plan-create'),
    path('api/plans/<int:pk>/', views.ProductionPlanDetailAPIView.as_view(), name='api-plan-detail'),
    path('api/batches/', views.ProductionBatchListAPIView.as_view(), name='api-batch-list'),
    path('api/batches/create/', views.ProductionBatchCreateAPIView.as_view(), name='api-batch-create'),
    path('api/batches/<int:pk>/', views.ProductionBatchDetailAPIView.as_view(), name='api-batch-detail'),
    path('api/quality/', views.QualityCheckListAPIView.as_view(), name='api-quality-list'),
    path('api/quality/create/', views.QualityCheckCreateAPIView.as_view(), name='api-quality-create'),
] 