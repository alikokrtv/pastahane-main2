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
from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer, OrderItemSerializer


class SalesListView(LoginRequiredMixin, ListView):
    """Satış listesi view'ı"""
    model = Order
    template_name = 'sales/sales_list.html'
    context_object_name = 'sales'
    paginate_by = 20
    
    def get_queryset(self):
        # Teslim edilmiş siparişleri satış olarak göster
        queryset = Order.objects.filter(status__in=['delivered', 'completed'])
        
        # Kullanıcının şubesine göre filtrele
        user = self.request.user
        if user.branch and user.role in ['branch_manager', 'cashier']:
            queryset = queryset.filter(branch=user.branch)
        
        return queryset.order_by('-created_at')


class SalesDetailView(LoginRequiredMixin, DetailView):
    """Satış detay view'ı"""
    model = Order
    template_name = 'sales/sales_detail.html'
    context_object_name = 'sale'
    
    def get_queryset(self):
        queryset = Order.objects.filter(status__in=['delivered', 'completed'])
        user = self.request.user
        if user.branch and user.role in ['branch_manager', 'cashier']:
            queryset = queryset.filter(branch=user.branch)
        return queryset


class DailySalesView(LoginRequiredMixin, TemplateView):
    """Günlük satış view'ı"""
    template_name = 'sales/daily_sales.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from django.utils import timezone
        today = timezone.now().date()
        
        # Günlük satış verileri
        daily_orders = Order.objects.filter(
            status__in=['delivered', 'completed'],
            created_at__date=today
        )
        
        user = self.request.user
        if user.branch and user.role in ['branch_manager', 'cashier']:
            daily_orders = daily_orders.filter(branch=user.branch)
        
        context['daily_orders'] = daily_orders
        context['daily_total'] = daily_orders.aggregate(
            total=Sum('total_amount')
        )['total'] or 0
        
        return context


class SalesReportView(LoginRequiredMixin, TemplateView):
    """Satış raporu view'ı"""
    template_name = 'sales/sales_report.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Satış raporları için gerekli veriler
        orders = Order.objects.filter(status__in=['delivered', 'completed'])
        
        user = self.request.user
        if user.branch and user.role in ['branch_manager', 'cashier']:
            orders = orders.filter(branch=user.branch)
        
        context['orders'] = orders
        context['total_sales'] = orders.aggregate(
            total=Sum('total_amount')
        )['total'] or 0
        
        return context


# API Views
class SalesListAPIView(generics.ListAPIView):
    """API Satış listesi"""
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Order.objects.filter(status__in=['delivered', 'completed'])
        user = self.request.user
        if user.branch and user.role in ['branch_manager', 'cashier']:
            queryset = queryset.filter(branch=user.branch)
        return queryset


class DailySalesAPIView(generics.ListAPIView):
    """API Günlük satış"""
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        from django.utils import timezone
        today = timezone.now().date()
        
        queryset = Order.objects.filter(
            status__in=['delivered', 'completed'],
            created_at__date=today
        )
        
        user = self.request.user
        if user.branch and user.role in ['branch_manager', 'cashier']:
            queryset = queryset.filter(branch=user.branch)
        
        return queryset


class SalesSummaryAPIView(generics.ListAPIView):
    """API Satış özet"""
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Order.objects.filter(status__in=['delivered', 'completed'])
        user = self.request.user
        if user.branch and user.role in ['branch_manager', 'cashier']:
            queryset = queryset.filter(branch=user.branch)
        return queryset
