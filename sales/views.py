from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView, View
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from datetime import datetime, timedelta
from rest_framework import generics, status, filters
import csv
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer, OrderItemSerializer
from .models import Satislar


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


class ViaposSalesListView(LoginRequiredMixin, TemplateView):
    """ViaPos 'satislar' tablosundaki TÜM satışlar için listeleme ve filtreleme"""
    template_name = 'sales/viapos_sales_list.html'

    def _detect_branch(self, cashier: str | None) -> str:
        name = (cashier or '').lower()
        if 'carsi' in name or 'çarşı' in name:
            return 'Çarşı'
        if 'vega' in name:
            return 'Vega'
        return 'Genel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = Satislar.objects.using('viapos').all().order_by('-tarih')

        # Filters
        q = self.request.GET.get('q')
        payment = self.request.GET.get('payment')
        group = self.request.GET.get('group')
        branch = self.request.GET.get('branch')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        if q:
            qs = qs.filter(Q(urun__icontains=q) | Q(musteriadi__icontains=q) | Q(fisno__icontains=q) | Q(barkod__icontains=q))
        if payment:
            qs = qs.filter(odemesi__iexact=payment)
        if group:
            qs = qs.filter(grub__icontains=group)
        if date_from:
            try:
                dtf = datetime.fromisoformat(date_from)
                qs = qs.filter(tarih__gte=dtf)
            except Exception:
                pass
        if date_to:
            try:
                dtt = datetime.fromisoformat(date_to)
                qs = qs.filter(tarih__lte=dtt)
            except Exception:
                pass

        # Branch filter via cashier mapping
        if branch:
            ids = [s.id for s in qs if self._detect_branch(getattr(s, 'satisiyapan', None)) == branch]
            qs = qs.filter(id__in=ids)

        # Aggregates
        total_amount = qs.aggregate(total=Sum('toplam'))['total'] or 0
        total_count = qs.count()

        # Pagination
        page = self.request.GET.get('page', 1)
        paginator = Paginator(qs, 25)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        # Prepare rows
        rows = []
        for s in page_obj.object_list:
            rows.append({
                'id': s.id,
                'fisno': s.fisno,
                'date': s.tarih,
                'customer': s.musteriadi,
                'product': s.urun,
                'group': getattr(s, 'grub', None),
                'quantity': s.adet,
                'price': s.fiyat,
                'amount': s.toplam,
                'profit': s.kar,
                'payment': s.odemesi,
                'cashier': s.satisiyapan,
                'branch': self._detect_branch(s.satisiyapan),
                'barcode': getattr(s, 'barkod', None),
            })

        context.update({
            'filters': {
                'q': q or '',
                'payment': payment or '',
                'group': group or '',
                'branch': branch or '',
                'date_from': date_from or '',
                'date_to': date_to or '',
            },
            'page_obj': page_obj,
            'paginator': paginator,
            'rows': rows,
            'total_amount': total_amount,
            'total_count': total_count,
        })

        return context


class ViaposSalesExportView(LoginRequiredMixin, View):
    """CSV export for ViaPos sales with same filters as list view"""
    def _detect_branch(self, cashier: str | None) -> str:
        name = (cashier or '').lower()
        if 'carsi' in name or 'çarşı' in name:
            return 'Çarşı'
        if 'vega' in name:
            return 'Vega'
        return 'Genel'

    def get(self, request):
        qs = Satislar.objects.using('viapos').all().order_by('-tarih')
        q = request.GET.get('q')
        payment = request.GET.get('payment')
        group = request.GET.get('group')
        branch = request.GET.get('branch')
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')

        if q:
            qs = qs.filter(Q(urun__icontains=q) | Q(musteriadi__icontains=q) | Q(fisno__icontains=q) | Q(barkod__icontains=q))
        if payment:
            qs = qs.filter(odemesi__iexact=payment)
        if group:
            qs = qs.filter(grub__icontains=group)
        if date_from:
            try:
                dtf = datetime.fromisoformat(date_from)
                qs = qs.filter(tarih__gte=dtf)
            except Exception:
                pass
        if date_to:
            try:
                dtt = datetime.fromisoformat(date_to)
                qs = qs.filter(tarih__lte=dtt)
            except Exception:
                pass
        if branch:
            ids = [s.id for s in qs if self._detect_branch(getattr(s, 'satisiyapan', None)) == branch]
            qs = qs.filter(id__in=ids)

        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="viapos_sales.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID','Fis No','Tarih','Müşteri','Ürün','Grup','Adet','Fiyat','Tutar','Kar','Ödeme','Kasiyer','Şube','Barkod'])
        for s in qs:
            writer.writerow([
                s.id,
                s.fisno,
                s.tarih,
                s.musteriadi,
                s.urun,
                getattr(s, 'grub', ''),
                s.adet,
                s.fiyat,
                s.toplam,
                s.kar,
                s.odemesi,
                s.satisiyapan,
                self._detect_branch(s.satisiyapan),
                getattr(s, 'barkod', ''),
            ])
        return response


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
