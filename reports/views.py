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


class ReportListView(LoginRequiredMixin, ListView):
    """Rapor listesi view'ı"""
    template_name = 'reports/report_list.html'
    context_object_name = 'reports'
    paginate_by = 20
    
    def get_queryset(self):
        # Geçici olarak boş queryset döndür
        from django.db import models
        return models.QuerySet(model=None)


class ReportDetailView(LoginRequiredMixin, DetailView):
    """Rapor detay view'ı"""
    template_name = 'reports/report_detail.html'
    context_object_name = 'report'
    
    def get_object(self):
        return None


class InventoryReportView(LoginRequiredMixin, TemplateView):
    """Envanter rapor view'ı"""
    template_name = 'reports/inventory_report.html'


class ProductionReportView(LoginRequiredMixin, TemplateView):
    """Üretim rapor view'ı"""
    template_name = 'reports/production_report.html'


class SalesReportView(LoginRequiredMixin, TemplateView):
    """Satış rapor view'ı"""
    template_name = 'reports/sales_report.html'


class DashboardReportView(LoginRequiredMixin, TemplateView):
    """Dashboard rapor view'ı"""
    template_name = 'reports/dashboard_report.html'


# API Views  
class ReportListAPIView(generics.GenericAPIView):
    """API Rapor listesi"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Rapor listesi
        data = {
            'reports': [],
            'count': 0,
            'status': 'success'
        }
        return Response(data)


class DashboardDataAPIView(generics.GenericAPIView):
    """API Dashboard data"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Dashboard için temel veriler
        data = {
            'total_orders': 0,
            'low_stock_count': 0,
            'active_users': 1,
            'daily_activities': 0,
            'status': 'success'
        }
        return Response(data)


class InventoryReportAPIView(generics.GenericAPIView):
    """API Envanter rapor"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Envanter raporu
        data = {
            'inventory': [],
            'count': 0,
            'status': 'success'
        }
        return Response(data)


class ProductionReportAPIView(generics.GenericAPIView):
    """API Üretim rapor"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Üretim raporu
        data = {
            'production': [],
            'count': 0,
            'status': 'success'
        }
        return Response(data)


class ActivityReportAPIView(generics.GenericAPIView):
    """API Aktivite rapor"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Aktivite verileri (şimdilik boş)
        data = {
            'activities': [],
            'count': 0,
            'status': 'success'
        }
        return Response(data)


class SalesReportAPIView(generics.GenericAPIView):
    """API Satış rapor"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Satış raporu
        data = {
            'sales': [],
            'count': 0,
            'status': 'success'
        }
        return Response(data)
