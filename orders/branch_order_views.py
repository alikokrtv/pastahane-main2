"""
Şube müdürleri için özel sipariş oluşturma view'ları
"""
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from inventory.models import Product, ProductCategory
from .models import Order, OrderItem, OrderStatusHistory
from users.models import Branch


class BranchOrderCreateView(LoginRequiredMixin, TemplateView):
    """Şube müdürleri için sipariş oluşturma arayüzü"""
    template_name = 'orders/branch_order_create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Aktif ürünleri kategorilere göre grupla
        categories = ProductCategory.objects.filter(
            is_active=True,
            products__is_active=True
        ).distinct().prefetch_related('products')
        
        # Ürünleri kategorilere göre organize et
        products_by_category = {}
        for category in categories:
            products = category.products.filter(is_active=True).order_by('name')
            if products.exists():
                products_by_category[category] = products
        
        # Yarın için varsayılan teslimat tarihi
        tomorrow = timezone.now().date() + timedelta(days=1)
        
        context.update({
            'products_by_category': products_by_category,
            'default_delivery_date': tomorrow,
            'user_branch': self.request.user.branch,
        })
        
        return context


@login_required
def create_branch_order_ajax(request):
    """AJAX ile şube siparişi oluştur"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Sadece POST istekleri kabul edilir'})
    
    try:
        data = json.loads(request.body)
        
        # Sipariş bilgilerini al
        delivery_date = data.get('delivery_date')
        notes = data.get('notes', '')
        order_items = data.get('items', [])
        
        if not delivery_date:
            return JsonResponse({'success': False, 'error': 'Teslimat tarihi gerekli'})
        
        if not order_items:
            return JsonResponse({'success': False, 'error': 'En az bir ürün seçmelisiniz'})
        
        # Teslimat tarihini parse et
        try:
            delivery_date = datetime.strptime(delivery_date, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Geçersiz tarih formatı'})
        
        # Bugünden önceki tarihleri kabul etme
        if delivery_date <= timezone.now().date():
            return JsonResponse({'success': False, 'error': 'Teslimat tarihi bugünden sonra olmalı'})
        
        with transaction.atomic():
            # Sipariş oluştur
            order = Order.objects.create(
                branch=request.user.branch,
                customer_name=f"{request.user.branch.name} - Günlük Sipariş",
                requested_delivery_date=delivery_date,
                notes=notes,
                priority='normal',
                status='pending',
                created_by=request.user
            )
            
            # Sipariş kalemlerini oluştur
            total_amount = 0
            for item_data in order_items:
                product_id = item_data.get('product_id')
                quantity = item_data.get('quantity', 0)
                
                if not product_id or quantity <= 0:
                    continue
                
                try:
                    product = Product.objects.get(id=product_id, is_active=True)
                except Product.DoesNotExist:
                    continue
                
                # Sipariş kalemi oluştur
                order_item = OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    unit_price=product.price_per_unit,
                    notes=item_data.get('notes', '')
                )
                
                total_amount += order_item.get_total_price()
            
            # Toplam tutarı güncelle
            order.subtotal = total_amount
            order.total_amount = total_amount
            order.save()
            
            # Durum geçmişi oluştur
            OrderStatusHistory.objects.create(
                order=order,
                from_status='',
                to_status='pending',
                changed_by=request.user,
                notes='Şube siparişi oluşturuldu'
            )
        
        return JsonResponse({
            'success': True,
            'message': 'Sipariş başarıyla oluşturuldu',
            'order_id': order.id,
            'order_number': order.order_number
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Geçersiz JSON verisi'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Sipariş oluşturulurken hata: {str(e)}'})


@login_required
def branch_order_list(request):
    """Şube siparişleri listesi"""
    # Kullanıcının şubesindeki siparişleri getir
    orders = Order.objects.filter(
        branch=request.user.branch
    ).select_related('branch', 'created_by').prefetch_related('items__product').order_by('-created_at')
    
    # Durum filtresi
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    # Tarih filtresi
    date_filter = request.GET.get('date')
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            orders = orders.filter(requested_delivery_date=filter_date)
        except ValueError:
            pass
    
    context = {
        'orders': orders,
        'status_choices': Order.STATUS_CHOICES,
        'selected_status': status_filter,
        'selected_date': date_filter,
    }
    
    return render(request, 'orders/branch_order_list.html', context)


@login_required
def branch_order_detail(request, order_id):
    """Şube sipariş detayı"""
    order = get_object_or_404(
        Order, 
        id=order_id, 
        branch=request.user.branch
    )
    
    # Sipariş kalemlerini getir
    order_items = OrderItem.objects.filter(
        order=order
    ).select_related('product')
    
    # Durum geçmişini getir
    status_history = OrderStatusHistory.objects.filter(
        order=order
    ).select_related('changed_by').order_by('-changed_at')
    
    context = {
        'order': order,
        'order_items': order_items,
        'status_history': status_history,
    }
    
    return render(request, 'orders/branch_order_detail.html', context)


@login_required
def update_order_status_ajax(request, order_id):
    """AJAX ile sipariş durumu güncelle"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Sadece POST istekleri kabul edilir'})
    
    try:
        order = Order.objects.get(id=order_id, branch=request.user.branch)
        data = json.loads(request.body)
        
        new_status = data.get('status')
        notes = data.get('notes', '')
        
        if new_status not in dict(Order.STATUS_CHOICES):
            return JsonResponse({'success': False, 'error': 'Geçersiz durum'})
        
        old_status = order.status
        order.status = new_status
        order.save()
        
        # Durum geçmişi kaydet
        OrderStatusHistory.objects.create(
            order=order,
            from_status=old_status,
            to_status=new_status,
            changed_by=request.user,
            notes=notes
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Sipariş durumu güncellendi',
            'new_status': new_status,
            'new_status_display': order.get_status_display()
        })
        
    except Order.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Sipariş bulunamadı'})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Geçersiz JSON verisi'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Durum güncellenirken hata: {str(e)}'})


@login_required
def production_orders_view(request):
    """Üretim bölümü için sipariş listesi"""
    # Onaylanmış ve üretimde olan siparişleri getir
    orders = Order.objects.filter(
        status__in=['confirmed', 'in_production']
    ).select_related('branch', 'created_by').prefetch_related('items__product').order_by('requested_delivery_date', 'created_at')
    
    # Yarının siparişlerini öne çıkar
    tomorrow = timezone.now().date() + timedelta(days=1)
    tomorrow_orders = orders.filter(requested_delivery_date=tomorrow)
    other_orders = orders.exclude(requested_delivery_date=tomorrow)
    
    context = {
        'tomorrow_orders': tomorrow_orders,
        'other_orders': other_orders,
        'tomorrow_date': tomorrow,
    }
    
    return render(request, 'orders/production_orders.html', context)


@login_required
def print_production_order(request, order_id):
    """Üretim siparişini yazdırma sayfası"""
    order = get_object_or_404(Order, id=order_id)
    
    # Sipariş kalemlerini kategorilere göre grupla
    order_items = OrderItem.objects.filter(
        order=order
    ).select_related('product', 'product__category').order_by('product__category__name', 'product__name')
    
    # Kategorilere göre grupla
    items_by_category = {}
    for item in order_items:
        category = item.product.category
        if category not in items_by_category:
            items_by_category[category] = []
        items_by_category[category].append(item)
    
    context = {
        'order': order,
        'items_by_category': items_by_category,
        'print_date': timezone.now(),
    }
    
    return render(request, 'orders/print_production_order.html', context)


@login_required
def simple_branch_order_create(request):
    """Şube müdürü için sade sipariş oluşturma sayfası"""
    if not request.user.branch:
        messages.error(request, 'Bir şubeye bağlı olmanız gerekiyor.')
        return redirect('users:login')
    
    # Aktif ürünleri kategoriye göre grupla
    products = Product.objects.filter(is_active=True).select_related('category').order_by('category__name', 'name')
    products_by_category = {}
    
    for product in products:
        category_name = product.category.name if product.category else 'Diğer'
        if category_name not in products_by_category:
            products_by_category[category_name] = []
        products_by_category[category_name].append(product)
    
    # Yarının tarihi
    tomorrow = timezone.now().date() + timedelta(days=1)
    today = timezone.now().date()
    
    context = {
        'products_by_category': products_by_category,
        'tomorrow': tomorrow,
        'today': today,
        'user': request.user,
    }
    
    return render(request, 'orders/simple_branch_order.html', context)
