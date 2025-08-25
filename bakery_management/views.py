from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Sum, Count, Q, F
from django.db.models.functions import TruncDate, TruncHour
from django.utils import timezone
from datetime import timedelta
import logging

from users.models import CustomUser, Branch
from inventory.models import Inventory, StockMovement, Product
from orders.models import Order
from sales.models import Satislar
from production.models import ProductionPlan, ProductionBatch

VIAPOS_AVAILABLE = True  # Satislar tablosunu kullanacağız

logger = logging.getLogger(__name__)


class DashboardView(LoginRequiredMixin, TemplateView):
    """Ana dashboard view'ı"""
    template_name = 'dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Bugün ve bu haftaki tarihler
        now = timezone.localtime()
        today = now.date()
        week_ago = today - timedelta(days=6)
        
        # Basit kasa/kasiyer -> şube tespiti (ihtiyaca göre genişletilebilir)
        def detect_branch(cashier: str | None) -> str:
            name = (cashier or '').lower()
            if 'carsi' in name or 'çarşı' in name:
                return 'Çarşı'
            if 'vega' in name:
                return 'Vega'
            return 'Genel'
        
        # Temel dashboard verileri
        context.update({
            'user': user,
            'today': today,
        })
        
        # ViaPos satislar verileri (external 'viapos' DB)
        try:
            tz = timezone.get_current_timezone()
            now = timezone.now().astimezone(tz)
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=1)

            qs_today = Satislar.objects.using('viapos').filter(tarih__gte=start, tarih__lt=end)
            # Bugün toplam ciro
            ciro = qs_today.aggregate(ciro=Sum('toplam'))['ciro'] or 0
            fis_sayisi = qs_today.values('fisno').distinct().count()
            satir = qs_today.count()
            ortalama_fis = (ciro / fis_sayisi) if fis_sayisi else 0

            # Son 7 gün ciro
            start7 = (now - timedelta(days=6)).replace(hour=0, minute=0, second=0, microsecond=0)
            qs7 = Satislar.objects.using('viapos').filter(tarih__date__gte=start7.date())
            ciro_son_7_gun = list(
                qs7.annotate(gun=TruncDate('tarih'))
                   .values('gun')
                   .annotate(ciro=Sum('toplam'))
                   .order_by('gun')
            )

            # Haftalık toplam ciro
            weekly_total = qs7.aggregate(total=Sum('toplam'))['total'] or 0

            # Son satışlar – şablonun beklediği yapıya dönüştür
            recent_qs = Satislar.objects.using('viapos').order_by('-tarih')[:10]
            recent_sales = [
                {
                    'customer': s.musteriadi,
                    'type': s.odemesi or 'Satış',
                    'amount': float(s.toplam or 0),
                    'date': s.tarih,
                    'product': s.urun,
                    'cashier': s.satisiyapan,
                    'payment': s.odemesi,
                    'barcode': getattr(s, 'barkod', None),
                    'group': getattr(s, 'grub', None),
                    'branch': detect_branch(s.satisiyapan),
                }
                for s in recent_qs
            ]

            # Bugün ürün bazında satış (miktar ve ciro)
            by_product_today = list(
                qs_today.values('urun')
                        .annotate(quantity=Sum('adet'), total=Sum('toplam'))
                        .order_by('-total')
            )

            # Bugün ödeme tipine göre ciro
            by_payment_today = list(
                qs_today.values('odemesi')
                        .annotate(total=Sum('toplam'))
                        .order_by('-total')
            )

            # Bugün şubeye göre ciro (Python tarafında tespit edilen branch ile)
            branch_totals = {}
            for s in qs_today:
                b = detect_branch(s.satisiyapan)
                branch_totals.setdefault(b, 0)
                branch_totals[b] += float(s.toplam or 0)
            by_branch_today = [{'branch': k, 'total': v} for k, v in sorted(branch_totals.items(), key=lambda x: -x[1])]

            # Bugün saatlik ciro
            saatlik = list(
                qs_today.annotate(saat=TruncHour('tarih'))
                        .values('saat')
                        .annotate(ciro=Sum('toplam'))
                        .order_by('saat')
            )

            context['viapos_data'] = {
                'ciro': ciro,
                'fis_sayisi': fis_sayisi,
                'satir': satir,
                'ortalama_fis': ortalama_fis,
                'ciro_son_7_gun': ciro_son_7_gun,
                'saatlik_satis_bugun': saatlik,
                # Template expectations
                'daily_total': ciro,
                'weekly_total': weekly_total,
                'recent_sales': recent_sales,
                'by_product_today': by_product_today,
                'by_payment_today': by_payment_today,
                'by_branch_today': by_branch_today,
            }
            context['viapos_available'] = True
        except Exception as e:
            logger.error(f"ViaPos veri çekme hatası: {e}")
            context['viapos_available'] = False
            context['viapos_error'] = str(e)
        
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