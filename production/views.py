from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.http import JsonResponse
from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import ProductionPlan, ProductionPlanItem, ProductionBatch, QualityCheck, ProductionReport


class ProductionPlanListView(LoginRequiredMixin, ListView):
    """Üretim planı listesi view'ı"""
    model = ProductionPlan
    template_name = 'production/plan_list.html'
    context_object_name = 'plans'
    paginate_by = 20
    
    def get_queryset(self):
        # Model'de branch alanı yoksa tüm planları göster
        queryset = ProductionPlan.objects.all()
        
        # Durum filtresi
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset.order_by('-created_at')


class ProductionPlanDetailView(LoginRequiredMixin, DetailView):
    """Üretim planı detay view'ı"""
    model = ProductionPlan
    template_name = 'production/plan_detail.html'
    context_object_name = 'plan'


class ProductionBatchListView(LoginRequiredMixin, ListView):
    """Üretim partisi listesi view'ı"""
    model = ProductionBatch
    template_name = 'production/batch_list.html'
    context_object_name = 'batches'
    paginate_by = 20
    
    def get_queryset(self):
        # Model'de branch alanı yoksa tüm partileri göster
        return ProductionBatch.objects.all().order_by('-created_at')


class ProductionBatchDetailView(LoginRequiredMixin, DetailView):
    """Üretim partisi detay view'ı"""
    model = ProductionBatch
    template_name = 'production/batch_detail.html'
    context_object_name = 'batch'


class QualityCheckListView(LoginRequiredMixin, ListView):
    """Kalite kontrol listesi view'ı"""
    model = QualityCheck
    template_name = 'production/quality_list.html'
    context_object_name = 'quality_checks'
    paginate_by = 20
    
    def get_queryset(self):
        # Model'de branch alanı yoksa tüm kalite kontrollerini göster
        return QualityCheck.objects.all().order_by('-created_at')


class ProductionReportListView(LoginRequiredMixin, ListView):
    """Üretim raporu listesi view'ı"""
    model = ProductionReport
    template_name = 'production/report_list.html'
    context_object_name = 'reports'
    paginate_by = 20
    
    def get_queryset(self):
        # Model'de branch alanı yoksa tüm raporları göster
        return ProductionReport.objects.all().order_by('-created_at')


# Missing Create Views
class ProductionPlanCreateView(LoginRequiredMixin, CreateView):
    """Üretim planı oluşturma view'ı"""
    model = ProductionPlan
    template_name = 'production/plan_create.html'
    fields = ['name', 'planned_date', 'notes']
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProductionBatchCreateView(LoginRequiredMixin, CreateView):
    """Üretim partisi oluşturma view'ı"""
    model = ProductionBatch
    template_name = 'production/batch_create.html'
    fields = ['batch_number', 'start_date', 'expected_end_date', 'notes']
    
    def form_valid(self, form):
        return super().form_valid(form)


# API Views
class ProductionPlanListAPIView(generics.ListAPIView):
    """API Üretim planı listesi"""
    model = ProductionPlan
    permission_classes = [IsAuthenticated]
    fields = ['name', 'planned_date', 'notes']
    
    def get_queryset(self):
        return ProductionPlan.objects.all()


class ProductionPlanCreateAPIView(generics.CreateAPIView):
    """API Üretim planı oluşturma"""
    model = ProductionPlan
    permission_classes = [IsAuthenticated]
    fields = ['name', 'planned_date', 'notes']


class ProductionPlanDetailAPIView(generics.RetrieveAPIView):
    """API Üretim planı detay"""
    model = ProductionPlan
    permission_classes = [IsAuthenticated]
    fields = ['name', 'planned_date', 'notes']
    
    def get_queryset(self):
        return ProductionPlan.objects.all()


class ProductionBatchListAPIView(generics.ListAPIView):
    """API Üretim partisi listesi"""
    model = ProductionBatch
    permission_classes = [IsAuthenticated]
    fields = ['batch_number', 'start_date', 'expected_end_date', 'notes']
    
    def get_queryset(self):
        return ProductionBatch.objects.all()


class ProductionBatchCreateAPIView(generics.CreateAPIView):
    """API Üretim partisi oluşturma"""
    model = ProductionBatch
    permission_classes = [IsAuthenticated]
    fields = ['batch_number', 'start_date', 'expected_end_date', 'notes']


class ProductionBatchDetailAPIView(generics.RetrieveAPIView):
    """API Üretim partisi detay"""
    model = ProductionBatch
    permission_classes = [IsAuthenticated]
    fields = ['batch_number', 'start_date', 'expected_end_date', 'notes']
    
    def get_queryset(self):
        return ProductionBatch.objects.all()


class QualityCheckListAPIView(generics.ListAPIView):
    """API Kalite kontrol listesi"""
    model = QualityCheck
    permission_classes = [IsAuthenticated]
    fields = ['batch', 'check_date', 'quality_score', 'notes']
    
    def get_queryset(self):
        return QualityCheck.objects.all()


class QualityCheckCreateAPIView(generics.CreateAPIView):
    """API Kalite kontrol oluşturma"""
    model = QualityCheck
    permission_classes = [IsAuthenticated]
    fields = ['batch', 'check_date', 'quality_score', 'notes']
