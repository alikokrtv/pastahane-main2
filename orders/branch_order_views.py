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


def format_order_for_whatsapp(order):
    """Sipariş bilgilerini WhatsApp için kategorili formatla"""
    lines = []
    lines.append("🏢 *TATO PASTA & BAKLAVA*")
    lines.append("📋 *ÜRETİM SİPARİŞİ*")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("")
    
    lines.append(f"📝 *Sipariş No:* {order.order_number}")
    lines.append(f"🏪 *Şube:* {order.branch.name}")
    lines.append(f"📅 *Teslimat:* {order.requested_delivery_date.strftime('%d.%m.%Y')}")
    lines.append(f"👤 *User ID:* {order.created_by.username}")
    lines.append(f"⏰ *Sipariş Zamanı:* {order.created_at.strftime('%d.%m.%Y %H:%M')}")
    
    if order.notes:
        lines.append(f"📌 *Özel Notlar:* {order.notes}")
    
    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("🍰 *ÜRETİM LİSTESİ*")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    # Ürünleri kategoriye göre grupla
    order_items = order.items.select_related('product', 'product__category').all()
    items_by_category = {}
    
    for item in order_items:
        category_name = item.product.category.name if item.product.category else 'DİĞER'
        if category_name not in items_by_category:
            items_by_category[category_name] = []
        items_by_category[category_name].append(item)
    
    total_quantity = 0
    category_totals = {}
    
    # Kategorileri sırala (Yeni Excel listesine göre)
    category_order = [
        'PASTA ÇEŞİTLERİ', 'DİLİM PASTALAR', 
        'TEPSİLİ ÜRÜNLER', 'SPESYAL ÜRÜNLER', 'SÜTLÜ TATLILAR', 
        'EKLER ÇEŞİTLERİ', 'DİĞER'
    ]
    
    for category_name in category_order:
        if category_name in items_by_category:
            items = items_by_category[category_name]
            category_total = 0
            
            lines.append("")
            lines.append(f"📂 *{category_name}*")
            lines.append("─────────────────────────────────")
            
            for item in items:
                quantity = int(item.quantity)
                unit = item.product.get_unit_display().upper()
                
                # WhatsApp formatı: İsim : Adet
                lines.append(f"• {item.product.name}: *{quantity} {unit}*")
                
                if item.notes:
                    lines.append(f"  💬 Not: _{item.notes}_")
                
                category_total += quantity
                total_quantity += quantity
            
            lines.append(f"📊 *{category_name} TOPLAM: {category_total} {unit}*")
            category_totals[category_name] = category_total
    
    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append(f"🎯 *GENEL TOPLAM: {total_quantity} ÜRÜN*")
    lines.append("")
    
    # Kategori özetleri
    lines.append("📋 *KATEGORİ ÖZETİ:*")
    for category_name, total in category_totals.items():
        lines.append(f"  • {category_name}: {total}")
    
    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("🏭 *TATO PASTA & BAKLAVA ÜRETİM*")
    
    return "\n".join(lines)


class BranchOrderCreateView(LoginRequiredMixin, TemplateView):
    """Şube müdürleri için sipariş oluşturma arayüzü"""
    template_name = 'orders/branch_order_create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Kategori sıralaması tanımla (PASTA ÇEŞİTLERİ en üstte)
        category_order = [
            'PASTA ÇEŞİTLERİ',
            'DİLİM PASTALAR', 
            'TEPSİLİ ÜRÜNLER',
            'SPESYAL ÜRÜNLER',
            'SÜTLÜ TATLILAR',
            'EKLER ÇEŞİTLERİ'
        ]
        
        # Aktif kategorileri al
        all_categories = ProductCategory.objects.filter(
            is_active=True,
            products__is_active=True
        ).distinct().prefetch_related('products')
        
        # Ürünleri kategorilere göre organize et (sıralı şekilde)
        products_by_category = {}
        
        # Önce belirtilen sırayla kategorileri ekle
        for category_name in category_order:
            try:
                category = all_categories.get(name=category_name)
                products = category.products.filter(is_active=True).order_by('name')
                if products.exists():
                    # Pasta çeşitleri için özel gruplandırma
                    if category_name == 'PASTA ÇEŞİTLERİ':
                        # Pasta çeşitlerini grupla (boyut bilgisini çıkar)
                        pasta_groups = {}
                        for product in products:
                            # "FISTIKLI BEYAZ - K4" -> "FISTIKLI BEYAZ"
                            if ' - ' in product.name:
                                base_name = product.name.split(' - ')[0]
                                size = product.name.split(' - ')[1]
                            else:
                                base_name = product.name
                                size = 'Standart'
                            
                            if base_name not in pasta_groups:
                                pasta_groups[base_name] = []
                            pasta_groups[base_name].append({
                                'size': size,
                                'product': product
                            })
                        
                        products_by_category[category] = pasta_groups
                    else:
                        products_by_category[category] = products
            except ProductCategory.DoesNotExist:
                continue
        
        # Sonra kalan kategorileri ekle (varsa)
        for category in all_categories:
            if category.name not in category_order:
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
    
    # GÜNLÜK SİPARİŞ KONTROLÜ - ŞİMDİLİK KAPALI (TEST İÇİN)
    # today = timezone.now().date()
    # existing_order_today = Order.objects.filter(
    #     branch=request.user.branch,
    #     created_by=request.user,
    #     created_at__date=today
    # ).exists()
    # 
    # if existing_order_today:
    #     return JsonResponse({
    #         'success': False, 
    #         'error': '⚠️ Bugün zaten sipariş verdiniz!\n\nGünde sadece 1 sipariş verebilirsiniz.\nMevcut siparişinizi düzenleyebilirsiniz.',
    #         'daily_limit_reached': True
    #     })
    
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
        
        # WhatsApp için sipariş formatını hazırla
        whatsapp_message = format_order_for_whatsapp(order)
        
        return JsonResponse({
            'success': True,
            'message': 'Sipariş başarıyla oluşturuldu',
            'order_id': order.id,
            'order_number': order.order_number,
            'show_whatsapp': True,
            'whatsapp_message': whatsapp_message
            # Telefon numarası artık gerekmiyor - kullanıcı kendisi seçecek
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


def categorize_products_for_factory(order_items):
    """Ürünleri fabrika yazdırma formatı için Excel kategorilerine ayır"""
    categories = {
        'PASTA_CESITLERI': [],  # En üste
        'DILIM_PASTALAR': [],
        'TEPSILI_URUNLER': [],  
        'SPESYAL_URUNLER': [],
        'SUTLU_TATLILAR': [],  
        'EKLER_CESITLERI': [],
        'DIGER': []
    }
    
    for item in order_items:
        # Önce ürünün kategorisine göre direkt eşleştir
        if item.product.category:
            category_name = item.product.category.name
            
            # Kategori adını template için uygun hale getir (Yeni Excel listesine göre)
            if category_name == 'PASTA ÇEŞİTLERİ':
                categories['PASTA_CESITLERI'].append(item)
            elif category_name == 'DİLİM PASTALAR':
                categories['DILIM_PASTALAR'].append(item)
            elif category_name == 'TEPSİLİ ÜRÜNLER':
                categories['TEPSILI_URUNLER'].append(item)
            elif category_name == 'SPESYAL ÜRÜNLER':
                categories['SPESYAL_URUNLER'].append(item)
            elif category_name == 'SÜTLÜ TATLILAR':
                categories['SUTLU_TATLILAR'].append(item)
            elif category_name == 'EKLER ÇEŞİTLERİ':
                categories['EKLER_CESITLERI'].append(item)
            else:
                categories['DIGER'].append(item)
        else:
            # Kategori yoksa isim bazında ayır (fallback)
            product_name = item.product.name.lower()
            
            if any(keyword in product_name for keyword in ['ekler', 'ek']):
                categories['EKLER_CESITLERI'].append(item)
            elif any(keyword in product_name for keyword in ['dilim', 'parça']):
                categories['DILIM_PASTALAR'].append(item)
            elif any(keyword in product_name for keyword in ['tepsi', 'sarma', 'rulo', 'malaga']):
                categories['TEPSILI_URUNLER'].append(item)
            elif any(keyword in product_name for keyword in ['bombası', 'şörözbek', 'özel']):
                categories['SPESYAL_URUNLER'].append(item)
            elif any(keyword in product_name for keyword in ['supangle', 'profiterol', 'magnolya', 'sütlü']):
                categories['SUTLU_TATLILAR'].append(item)
            else:
                # Diğer her şey pasta çeşitleri kategorisine gider
                categories['PASTA_CESITLERI'].append(item)
    
    return categories


@login_required
def print_factory_order(request, order_id):
    """Fabrika formatında sipariş yazdırma sayfası"""
    order = get_object_or_404(Order, id=order_id)
    
    # Sipariş kalemlerini al
    order_items = OrderItem.objects.filter(
        order=order
    ).select_related('product', 'product__category').order_by('product__name')
    
    # Ürünleri fabrika kategorilerine göre ayır
    categories = categorize_products_for_factory(order_items)
    
    # Toplam ürün sayısını hesapla
    total_items = sum(int(item.quantity) for item in order_items)
    
    context = {
        'order': order,
        'categories': categories,
        'total_items': total_items,
        'print_date': timezone.now(),
    }
    
    return render(request, 'orders/print_factory_order.html', context)


@login_required
def simple_branch_order_create(request):
    """Şube müdürü için sade sipariş oluşturma sayfası"""
    if not request.user.branch:
        messages.error(request, 'Bir şubeye bağlı olmanız gerekiyor.')
        return redirect('users:login')
    
    # Kategori sıralaması tanımla (PASTA ÇEŞİTLERİ en üstte)
    category_order = [
        'PASTA ÇEŞİTLERİ',
        'DİLİM PASTALAR', 
        'TEPSİLİ ÜRÜNLER',
        'SPESYAL ÜRÜNLER',
        'SÜTLÜ TATLILAR',
        'EKLER ÇEŞİTLERİ'
    ]
    
    # Aktif ürünleri al
    products = Product.objects.filter(is_active=True).select_related('category').order_by('name')
    
    # Ürünleri kategorilere göre organize et (sıralı şekilde)
    products_by_category = {}
    
    # Önce belirtilen sırayla kategorileri ekle
    for category_name in category_order:
        category_products = [p for p in products if p.category and p.category.name == category_name]
        if category_products:
            # Pasta çeşitleri için özel gruplandırma
            if category_name == 'PASTA ÇEŞİTLERİ':
                pasta_groups = {}
                for product in category_products:
                    # "FISTIKLI BEYAZ - K4" -> "FISTIKLI BEYAZ"
                    if ' - ' in product.name:
                        base_name = product.name.split(' - ')[0]
                        size = product.name.split(' - ')[1]
                    else:
                        base_name = product.name
                        size = 'Standart'
                    
                    if base_name not in pasta_groups:
                        pasta_groups[base_name] = []
                    pasta_groups[base_name].append({
                        'size': size,
                        'product': product
                    })
                
                products_by_category[category_name] = pasta_groups
            else:
                products_by_category[category_name] = category_products
    
    # Sonra kalan kategorileri ekle (varsa)
    for product in products:
        if product.category:
            category_name = product.category.name
            if category_name not in category_order and category_name not in products_by_category:
                remaining_products = [p for p in products if p.category and p.category.name == category_name]
                products_by_category[category_name] = remaining_products
        else:
            # Kategorisi olmayan ürünler
            if 'Diğer' not in products_by_category:
                products_by_category['Diğer'] = []
            if product not in products_by_category['Diğer']:
                products_by_category['Diğer'].append(product)
    
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
