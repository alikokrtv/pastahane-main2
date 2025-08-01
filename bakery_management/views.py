from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Sum, Count, Q, F
from django.utils import timezone
from datetime import timedelta

from users.models import CustomUser, Branch
from inventory.models import Inventory, StockMovement, Product
from orders.models import Order
from production.models import ProductionPlan, ProductionBatch


class DashboardView(LoginRequiredMixin, TemplateView):
    """Ana dashboard view'ı"""
    template_name = 'dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Bugün ve bu hafta tarihleri
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        
        # Temel dashboard verileri
        context.update({
            'user': user,
            'today': today,
        })
        
        # Kullanıcının şube bilgileri
        if user.branch:
            branch_stats = self._get_branch_statistics(user.branch, today, week_ago)
            context.update(branch_stats)
        
        # Rol bazlı özel veriler
        if user.role in ['admin', 'manager']:
            admin_stats = self._get_admin_statistics(today, week_ago)
            context.update(admin_stats)
        elif user.role == 'production_manager':
            production_stats = self._get_production_statistics(user.branch, today)
            context.update(production_stats)
        elif user.role in ['branch_manager', 'cashier']:
            branch_sales_stats = self._get_branch_sales_statistics(user.branch, today)
            context.update(branch_sales_stats)
        
        return context
    
    def _get_branch_statistics(self, branch, today, week_ago):
        """Şube istatistikleri"""
        stats = {}
        
        # Stok durumu
        if hasattr(branch, 'inventory_set'):
            inventories = Inventory.objects.filter(branch=branch)
            stats.update({
                'total_products': inventories.count(),
                'low_stock_items': inventories.filter(
                    current_stock__lte=F('min_stock_level')
                ).count(),
                'out_of_stock_items': inventories.filter(current_stock=0).count(),
            })
        
        # Bu haftaki siparişler
        weekly_orders = Order.objects.filter(
            branch=branch,
            created_at__date__gte=week_ago
        )
        
        stats.update({
            'weekly_orders': weekly_orders.count(),
            'pending_orders': weekly_orders.filter(status='pending').count(),
            'completed_orders': weekly_orders.filter(status='delivered').count(),
        })
        
        return stats
    
    def _get_admin_statistics(self, today, week_ago):
        """Admin istatistikleri"""
        stats = {}
        
        # Genel sistem istatikleri
        stats.update({
            'total_branches': Branch.objects.filter(is_active=True).count(),
            'total_users': CustomUser.objects.filter(is_active=True).count(),
            'total_products': Product.objects.filter(is_active=True).count(),
        })
        
        # Bu haftaki toplam siparişler
        weekly_orders = Order.objects.filter(created_at__date__gte=week_ago)
        stats.update({
            'weekly_total_orders': weekly_orders.count(),
            'weekly_revenue': weekly_orders.aggregate(
                total=Sum('total_amount')
            )['total'] or 0,
        })
        
        return stats
    
    def _get_production_statistics(self, branch, today):
        """Üretim istatistikleri"""
        stats = {}
        
        if branch and branch.branch_type == 'production_center':
            # Bugünkü üretim planları
            today_plans = ProductionPlan.objects.filter(
                branch=branch,
                planned_date=today
            )
            
            # Aktif partiler
            active_batches = ProductionBatch.objects.filter(
                branch=branch,
                status__in=['planned', 'in_progress']
            )
            
            stats.update({
                'today_production_plans': today_plans.count(),
                'active_batches': active_batches.count(),
                'completed_batches_today': ProductionBatch.objects.filter(
                    branch=branch,
                    end_date=today,
                    status='completed'
                ).count(),
            })
        
        return stats
    
    def _get_branch_sales_statistics(self, branch, today):
        """Şube satış istatikleri"""
        stats = {}
        
        # Bugünkü siparişler
        today_orders = Order.objects.filter(
            branch=branch,
            created_at__date=today
        )
        
        stats.update({
            'today_orders': today_orders.count(),
            'today_revenue': today_orders.aggregate(
                total=Sum('total_amount')
            )['total'] or 0,
            'ready_for_delivery': Order.objects.filter(
                branch=branch,
                status='ready'
            ).count(),
        })
        
        return stats


@login_required
def dashboard(request):
    """Dashboard view function (alternatif)"""
    return DashboardView.as_view()(request)


def home(request):
    """Ana sayfa - giriş kontrolü"""
    if request.user.is_authenticated:
        # Giriş yapmış kullanıcıları uygun sayfaya yönlendir
        if hasattr(request.user, 'role') and request.user.role == 'branch_manager':
            return redirect('orders:branch_order_create')
        elif request.user.branch and not request.user.is_staff:
            return redirect('orders:branch_order_create')
        else:
            return redirect('dashboard')
    else:
        return redirect('users:login') 