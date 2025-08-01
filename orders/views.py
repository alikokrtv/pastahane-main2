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
from .models import (
    Order, OrderItem, OrderStatusHistory, DeliveryRoute, 
    Delivery, OrderTemplate, OrderTemplateItem
)
from .serializers import (
    OrderSerializer, OrderItemSerializer, DeliverySerializer,
    OrderTemplateSerializer
)


class OrderListView(LoginRequiredMixin, ListView):
    """Sipariş listesi view'ı"""
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    paginate_by = 20
    
    def get_queryset(self):
        # Kullanıcının rolüne göre siparişleri filtrele
        queryset = Order.objects.select_related('branch')
        
        user = self.request.user
        if user.role in ['branch_manager', 'cashier']:
            # Şube yöneticisi ve kasiyer sadece kendi şubelerindeki siparişleri görebilir
            queryset = queryset.filter(branch=user.branch)
        elif user.role == 'delivery':
            # Kurye sadece kendi teslimatlarını görebilir
            queryset = queryset.filter(delivery__driver=user)
        
        # Durum filtresi
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Arama filtresi
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(order_number__icontains=search) |
                Q(customer_name__icontains=search) |
                Q(customer_phone__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # İstatistikler
        if user.branch:
            orders = Order.objects.filter(branch=user.branch)
            context.update({
                'pending_orders': orders.filter(status='pending').count(),
                'confirmed_orders': orders.filter(status='confirmed').count(),
                'in_production_orders': orders.filter(status='in_production').count(),
                'ready_orders': orders.filter(status='ready').count(),
            })
        
        return context


class OrderDetailView(LoginRequiredMixin, DetailView):
    """Sipariş detay view'ı"""
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        
        # Sipariş kalemleri
        context['order_items'] = OrderItem.objects.filter(
            order=order
        ).select_related('product')
        
        # Durum geçmişi
        context['status_history'] = OrderStatusHistory.objects.filter(
            order=order
        ).select_related('changed_by')
        
        # Teslimat bilgileri
        try:
            context['delivery'] = Delivery.objects.get(order=order)
        except Delivery.DoesNotExist:
            context['delivery'] = None
        
        return context


class OrderCreateView(LoginRequiredMixin, CreateView):
    """Sipariş oluşturma view'ı"""
    model = Order
    template_name = 'orders/order_create.html'
    fields = ['customer_name', 'customer_phone', 'requested_delivery_date', 
              'notes', 'priority']
    
    def form_valid(self, form):
        form.instance.branch = self.request.user.branch
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    """Sipariş güncelleme view'ı"""
    model = Order
    template_name = 'orders/order_edit.html'
    fields = ['customer_name', 'customer_phone', 'requested_delivery_date', 
              'notes', 'priority', 'status']


class DeliveryListView(LoginRequiredMixin, ListView):
    """Teslimat listesi view'ı"""
    model = Delivery
    template_name = 'orders/delivery_list.html'
    context_object_name = 'deliveries'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Delivery.objects.select_related('order', 'driver', 'route')
        
        user = self.request.user
        if user.role == 'delivery':
            # Kurye sadece kendi teslimatlarını görebilir
            queryset = queryset.filter(driver=user)
        elif user.role in ['branch_manager', 'cashier']:
            # Şube personeli kendi şubelerindeki teslimatları görebilir
            queryset = queryset.filter(order__branch=user.branch)
        
        # Durum filtresi
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset.order_by('-delivery_address')


class OrderTemplateListView(LoginRequiredMixin, ListView):
    """Sipariş şablonu listesi view'ı"""
    model = OrderTemplate
    template_name = 'orders/template_list.html'
    context_object_name = 'templates'
    paginate_by = 20
    
    def get_queryset(self):
        # Kullanıcının şubesindeki şablonları göster
        return OrderTemplate.objects.filter(
            branch=self.request.user.branch,
            is_active=True
        ).order_by('name')


# API Views
class OrderListAPIView(generics.ListCreateAPIView):
    """API Sipariş listesi ve oluşturma"""
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['order_number', 'customer_name', 'customer_phone']
    filterset_fields = ['status', 'priority']
    
    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.select_related('branch')
        
        if user.role in ['branch_manager', 'cashier']:
            queryset = queryset.filter(branch=user.branch)
        elif user.role == 'delivery':
            queryset = queryset.filter(delivery__driver=user)
        
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            branch=self.request.user.branch
        )


class OrderDetailAPIView(generics.RetrieveUpdateAPIView):
    """API Sipariş detay ve güncelleme"""
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.select_related('branch')
        
        if user.role in ['branch_manager', 'cashier']:
            queryset = queryset.filter(branch=user.branch)
        elif user.role == 'delivery':
            queryset = queryset.filter(delivery__driver=user)
        
        return queryset


class DeliveryListAPIView(generics.ListAPIView):
    """API Teslimat listesi"""
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    
    def get_queryset(self):
        user = self.request.user
        queryset = Delivery.objects.select_related('order', 'driver', 'route')
        
        if user.role == 'delivery':
            queryset = queryset.filter(driver=user)
        elif user.role in ['branch_manager', 'cashier']:
            queryset = queryset.filter(order__branch=user.branch)
        
        return queryset.order_by('-delivery_date')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_order_status_api(request, order_id):
    """Sipariş durumu güncelleme API'si"""
    try:
        order = Order.objects.get(id=order_id)
        
        # Yetki kontrolü
        user = request.user
        if user.role in ['branch_manager', 'cashier']:
            if order.branch != user.branch:
                return Response({'error': 'Bu siparişi güncelleme yetkiniz yok'}, 
                               status=status.HTTP_403_FORBIDDEN)
        
        new_status = request.data.get('status')
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response({'error': 'Geçersiz durum'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        old_status = order.status
        order.status = new_status
        order.save()
        
        # Durum geçmişi kaydet
        OrderStatusHistory.objects.create(
            order=order,
            old_status=old_status,
            new_status=new_status,
            changed_by=user,
            notes=request.data.get('notes', '')
        )
        
        return Response({
            'status': 'success',
            'message': 'Sipariş durumu güncellendi',
            'order_status': new_status
        })
        
    except Order.DoesNotExist:
        return Response({'error': 'Sipariş bulunamadı'}, 
                       status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order_from_template_api(request, template_id):
    """Şablondan sipariş oluşturma API'si"""
    try:
        template = OrderTemplate.objects.get(id=template_id, branch=request.user.branch)
        
        # Yeni sipariş oluştur
        order_data = request.data.copy()
        order = Order.objects.create(
            customer_name=order_data.get('customer_name'),
            customer_phone=order_data.get('customer_phone'),
            customer_email=order_data.get('customer_email', ''),
            delivery_address=order_data.get('delivery_address', ''),
            delivery_date=order_data.get('delivery_date'),
            special_instructions=order_data.get('special_instructions', ''),
            branch=request.user.branch,
            created_by=request.user
        )
        
        # Şablon kalemlerini kopyala
        template_items = OrderTemplateItem.objects.filter(template=template)
        for item in template_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                unit_price=item.product.selling_price,
                total_price=item.quantity * item.product.selling_price
            )
        
        # Toplam tutarı hesapla
        order.calculate_totals()
        
        return Response({
            'status': 'success',
            'message': 'Sipariş şablondan oluşturuldu',
            'order_id': order.id,
            'order_number': order.order_number
        })
        
    except OrderTemplate.DoesNotExist:
        return Response({'error': 'Şablon bulunamadı'}, 
                       status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_statistics_api(request):
    """Sipariş istatistikleri API'si"""
    user = request.user
    
    # Kullanıcının şubesindeki siparişler
    orders = Order.objects.filter(branch=user.branch)
    
    # Bugünkü siparişler
    from django.utils import timezone
    today = timezone.now().date()
    today_orders = orders.filter(created_at__date=today)
    
    statistics = {
        'total_orders': orders.count(),
        'today_orders': today_orders.count(),
        'pending_orders': orders.filter(status='pending').count(),
        'confirmed_orders': orders.filter(status='confirmed').count(),
        'in_production_orders': orders.filter(status='in_production').count(),
        'ready_orders': orders.filter(status='ready').count(),
        'delivered_orders': orders.filter(status='delivered').count(),
        'cancelled_orders': orders.filter(status='cancelled').count(),
    }
    
    return Response(statistics)


from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])
def factory_orders_api(request):
    """Fabrika için yeni siparişleri dinleme API'si (Kimlik doğrulama gerektirmez)"""
    # Token tabanlı basit güvenlik
    auth_token = request.GET.get('token')
    if auth_token != 'factory_printer_2024':
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Yeni onaylanan siparişleri getir (son 24 saat)
    from django.utils import timezone
    from datetime import timedelta
    
    yesterday = timezone.now() - timedelta(hours=24)
    
    # Onaylanmış veya üretimde olan siparişleri getir
    orders = Order.objects.filter(
        status__in=['confirmed', 'pending'],
        created_at__gte=yesterday
    ).select_related('branch', 'created_by').prefetch_related('items__product')
    
    # Son kontrol edilen zamanı parametreden al
    last_check = request.GET.get('last_check')
    if last_check:
        try:
            from datetime import datetime
            last_check_time = datetime.fromisoformat(last_check.replace('Z', '+00:00'))
            orders = orders.filter(created_at__gte=last_check_time)
        except:
            pass  # Hatalı format, tüm siparişleri getir
    
    # Sipariş verilerini hazırla
    orders_data = []
    for order in orders:
        items_data = []
        for item in order.items.all():
            items_data.append({
                'product_name': item.product.name,
                'quantity': float(item.quantity),
                'unit': item.product.get_unit_display(),
                'notes': item.notes
            })
        
        orders_data.append({
            'id': order.id,
            'order_number': order.order_number,
            'branch_name': order.branch.name,
            'customer_name': order.customer_name,
            'delivery_date': order.requested_delivery_date.isoformat(),
            'status': order.get_status_display(),
            'notes': order.notes,
            'created_at': order.created_at.isoformat(),
            'total_amount': float(order.total_amount),
            'items': items_data,
            'created_by': order.created_by.get_full_name() or order.created_by.username
        })
    
    return Response({
        'orders': orders_data,
        'count': len(orders_data),
        'timestamp': timezone.now().isoformat()
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def mark_order_printed_api(request):
    """Siparişin yazdırıldığını işaretle"""
    auth_token = request.data.get('token')
    if auth_token != 'factory_printer_2024':
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    
    order_id = request.data.get('order_id')
    if not order_id:
        return Response({'error': 'order_id required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        order = Order.objects.get(id=order_id)
        
        # Sipariş durumunu 'in_production' yap
        if order.status == 'pending':
            order.status = 'confirmed'
            order.save()
            
            # Durum geçmişi kaydet
            OrderStatusHistory.objects.create(
                order=order,
                from_status='pending',
                to_status='confirmed',
                changed_by_id=1,  # System user
                notes='Fabrika yazıcısından yazdırıldı'
            )
        
        return Response({
            'success': True,
            'message': 'Sipariş yazdırıldı olarak işaretlendi',
            'order_number': order.order_number
        })
        
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
