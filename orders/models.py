from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta


User = get_user_model()


class Order(models.Model):
    """Sipariş modeli"""
    STATUS_CHOICES = [
        ('draft', 'Taslak'),
        ('pending', 'Beklemede'),
        ('confirmed', 'Onaylandı'),
        ('in_production', 'Üretimde'),
        ('ready', 'Hazır'),
        ('out_for_delivery', 'Yolda'),
        ('delivered', 'Teslim Edildi'),
        ('cancelled', 'İptal Edildi'),
        ('returned', 'İade Edildi'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Düşük'),
        ('normal', 'Normal'),
        ('high', 'Yüksek'),
        ('urgent', 'Acil'),
    ]
    
    order_number = models.CharField(_('Sipariş No'), max_length=50, unique=True)
    branch = models.ForeignKey(
        'users.Branch',
        on_delete=models.CASCADE,
        verbose_name=_('Şube'),
        related_name='orders'
    )
    customer_name = models.CharField(_('Müşteri Adı'), max_length=200, blank=True)
    customer_phone = models.CharField(_('Müşteri Telefon'), max_length=20, blank=True)
    status = models.CharField(_('Durum'), max_length=20, choices=STATUS_CHOICES, default='draft')
    priority = models.CharField(_('Öncelik'), max_length=10, choices=PRIORITY_CHOICES, default='normal')
    
    order_date = models.DateField(_('Sipariş Tarihi'), default=timezone.now)
    requested_delivery_date = models.DateField(_('İstenen Teslimat Tarihi'))
    actual_delivery_date = models.DateTimeField(_('Gerçek Teslimat Tarihi'), blank=True, null=True)
    
    notes = models.TextField(_('Notlar'), blank=True)
    internal_notes = models.TextField(_('İç Notlar'), blank=True, help_text='Sadece personel görebilir')
    
    # Fiyat bilgileri
    subtotal = models.DecimalField(
        _('Ara Toplam'),
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )
    discount_amount = models.DecimalField(
        _('İndirim Tutarı'),
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )
    tax_amount = models.DecimalField(
        _('KDV Tutarı'),
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )
    total_amount = models.DecimalField(
        _('Toplam Tutar'),
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )
    
    # İzleme bilgileri
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Oluşturan'), related_name='created_orders')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Atanan'), related_name='assigned_orders')
    created_at = models.DateTimeField(_('Oluşturulma Tarihi'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Güncellenme Tarihi'), auto_now=True)
    
    class Meta:
        verbose_name = _('Sipariş')
        verbose_name_plural = _('Siparişler')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order_number']),
            models.Index(fields=['status']),
            models.Index(fields=['requested_delivery_date']),
            models.Index(fields=['branch', 'status']),
        ]
    
    def __str__(self):
        return f"{self.order_number} - {self.branch.name} - {self.get_status_display()}"
    
    def save(self, *args, **kwargs):
        """Sipariş numarası otomatik oluştur"""
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)
    
    def generate_order_number(self):
        """Sipariş numarası oluştur"""
        today = timezone.now().date()
        branch_code = self.branch.name[:3].upper() if self.branch else 'GEN'
        date_str = today.strftime('%Y%m%d')
        
        # Bugün bu şube için kaçıncı sipariş
        daily_count = Order.objects.filter(
            branch=self.branch,
            created_at__date=today
        ).count() + 1
        
        return f"{branch_code}-{date_str}-{daily_count:03d}"
    
    def calculate_totals(self):
        """Toplam tutarları hesapla"""
        self.subtotal = sum(item.get_total_price() for item in self.items.all())
        self.tax_amount = self.subtotal * Decimal('0.18')  # %18 KDV
        self.total_amount = self.subtotal + self.tax_amount - self.discount_amount
        self.save()
    
    def get_item_count(self):
        """Toplam ürün sayısını döndürür"""
        return sum(item.quantity for item in self.items.all())
    
    def is_overdue(self):
        """Teslimat tarihi geçti mi?"""
        if self.status in ['delivered', 'cancelled', 'returned']:
            return False
        return timezone.now().date() > self.requested_delivery_date
    
    def can_be_cancelled(self):
        """İptal edilebilir mi?"""
        return self.status in ['draft', 'pending', 'confirmed']
    
    def can_be_modified(self):
        """Değiştirilebilir mi?"""
        return self.status in ['draft', 'pending']
    
    def get_estimated_completion_time(self):
        """Tahmini tamamlanma süresini döndürür"""
        total_time = sum(
            item.product.recipe.preparation_time + item.product.recipe.cooking_time
            if hasattr(item.product, 'recipe') and item.product.recipe
            else 60  # Default 60 dakika
            for item in self.items.all()
        )
        return timedelta(minutes=total_time)


class OrderItem(models.Model):
    """Sipariş kalemleri"""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name=_('Sipariş'),
        related_name='items'
    )
    product = models.ForeignKey(
        'inventory.Product',
        on_delete=models.CASCADE,
        verbose_name=_('Ürün'),
        related_name='order_items'
    )
    quantity = models.DecimalField(
        _('Miktar'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    unit_price = models.DecimalField(
        _('Birim Fiyat'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    discount_percentage = models.DecimalField(
        _('İndirim Oranı (%)'),
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    notes = models.CharField(_('Notlar'), max_length=500, blank=True)
    created_at = models.DateTimeField(_('Oluşturulma Tarihi'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Sipariş Kalemi')
        verbose_name_plural = _('Sipariş Kalemleri')
        unique_together = ['order', 'product']
    
    def __str__(self):
        return f"{self.order.order_number} - {self.product.name} x {self.quantity}"
    
    def save(self, *args, **kwargs):
        """Birim fiyatı otomatik ayarla"""
        if not self.unit_price:
            self.unit_price = self.product.price_per_unit
        super().save(*args, **kwargs)
        # Sipariş toplamlarını güncelle
        self.order.calculate_totals()
    
    def get_subtotal(self):
        """İndirim öncesi toplam fiyat"""
        return self.quantity * self.unit_price
    
    def get_discount_amount(self):
        """İndirim tutarı"""
        return self.get_subtotal() * (self.discount_percentage / 100)
    
    def get_total_price(self):
        """İndirimli toplam fiyat"""
        return self.get_subtotal() - self.get_discount_amount()


class OrderStatusHistory(models.Model):
    """Sipariş durum geçmişi"""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name=_('Sipariş'),
        related_name='status_history'
    )
    from_status = models.CharField(_('Önceki Durum'), max_length=20, choices=Order.STATUS_CHOICES, blank=True)
    to_status = models.CharField(_('Yeni Durum'), max_length=20, choices=Order.STATUS_CHOICES)
    notes = models.TextField(_('Notlar'), blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Değiştiren'))
    changed_at = models.DateTimeField(_('Değiştirilme Tarihi'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Sipariş Durum Geçmişi')
        verbose_name_plural = _('Sipariş Durum Geçmişleri')
        ordering = ['-changed_at']
    
    def __str__(self):
        return f"{self.order.order_number} - {self.get_to_status_display()}"


class DeliveryRoute(models.Model):
    """Teslimat rotası"""
    name = models.CharField(_('Rota Adı'), max_length=100)
    description = models.TextField(_('Açıklama'), blank=True)
    delivery_areas = models.TextField(_('Teslimat Bölgeleri'), help_text='Virgülle ayırarak yazın')
    estimated_duration = models.IntegerField(_('Tahmini Süre (dakika)'), default=60)
    is_active = models.BooleanField(_('Aktif'), default=True)
    created_at = models.DateTimeField(_('Oluşturulma Tarihi'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Teslimat Rotası')
        verbose_name_plural = _('Teslimat Rotaları')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Delivery(models.Model):
    """Teslimat takibi"""
    STATUS_CHOICES = [
        ('planned', 'Planlandı'),
        ('assigned', 'Atandı'),
        ('in_progress', 'Yolda'),
        ('delivered', 'Teslim Edildi'),
        ('failed', 'Başarısız'),
        ('returned', 'İade Edildi'),
    ]
    
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        verbose_name=_('Sipariş'),
        related_name='delivery'
    )
    route = models.ForeignKey(
        DeliveryRoute,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Rota'),
        related_name='deliveries'
    )
    driver = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Sürücü'),
        related_name='deliveries'
    )
    status = models.CharField(_('Durum'), max_length=20, choices=STATUS_CHOICES, default='planned')
    
    delivery_address = models.TextField(_('Teslimat Adresi'))
    delivery_phone = models.CharField(_('Teslimat Telefon'), max_length=20)
    delivery_contact = models.CharField(_('Teslimat İletişim'), max_length=200)
    
    planned_start_time = models.DateTimeField(_('Planlanan Başlangıç'))
    actual_start_time = models.DateTimeField(_('Gerçek Başlangıç'), blank=True, null=True)
    planned_end_time = models.DateTimeField(_('Planlanan Bitiş'))
    actual_end_time = models.DateTimeField(_('Gerçek Bitiş'), blank=True, null=True)
    
    delivery_notes = models.TextField(_('Teslimat Notları'), blank=True)
    customer_signature = models.TextField(_('Müşteri İmza'), blank=True)
    delivery_photo = models.ImageField(_('Teslimat Fotoğrafı'), upload_to='deliveries/', blank=True, null=True)
    
    created_at = models.DateTimeField(_('Oluşturulma Tarihi'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Güncellenme Tarihi'), auto_now=True)
    
    class Meta:
        verbose_name = _('Teslimat')
        verbose_name_plural = _('Teslimatlar')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.order.order_number} - {self.get_status_display()}"
    
    def is_overdue(self):
        """Teslimat gecikti mi?"""
        if self.status in ['delivered', 'failed', 'returned']:
            return False
        return timezone.now() > self.planned_end_time
    
    def get_duration(self):
        """Teslimat süresini döndürür"""
        if self.actual_start_time and self.actual_end_time:
            return self.actual_end_time - self.actual_start_time
        return None


class OrderTemplate(models.Model):
    """Sipariş şablonu - Tekrarlayan siparişler için"""
    name = models.CharField(_('Şablon Adı'), max_length=200)
    branch = models.ForeignKey(
        'users.Branch',
        on_delete=models.CASCADE,
        verbose_name=_('Şube'),
        related_name='order_templates'
    )
    description = models.TextField(_('Açıklama'), blank=True)
    is_active = models.BooleanField(_('Aktif'), default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Oluşturan'))
    created_at = models.DateTimeField(_('Oluşturulma Tarihi'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Güncellenme Tarihi'), auto_now=True)
    
    class Meta:
        verbose_name = _('Sipariş Şablonu')
        verbose_name_plural = _('Sipariş Şablonları')
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.branch.name}"
    
    def create_order_from_template(self, delivery_date, user):
        """Şablondan sipariş oluştur"""
        order = Order.objects.create(
            branch=self.branch,
            requested_delivery_date=delivery_date,
            notes=f"Şablondan oluşturuldu: {self.name}",
            created_by=user
        )
        
        # Şablon kalemlerini kopyala
        for template_item in self.items.all():
            OrderItem.objects.create(
                order=order,
                product=template_item.product,
                quantity=template_item.quantity,
                unit_price=template_item.product.price_per_unit,
                notes=template_item.notes
            )
        
        order.calculate_totals()
        return order


class OrderTemplateItem(models.Model):
    """Sipariş şablonu kalemleri"""
    template = models.ForeignKey(
        OrderTemplate,
        on_delete=models.CASCADE,
        verbose_name=_('Şablon'),
        related_name='items'
    )
    product = models.ForeignKey(
        'inventory.Product',
        on_delete=models.CASCADE,
        verbose_name=_('Ürün'),
        related_name='template_items'
    )
    quantity = models.DecimalField(
        _('Miktar'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    notes = models.CharField(_('Notlar'), max_length=500, blank=True)
    
    class Meta:
        verbose_name = _('Sipariş Şablonu Kalemi')
        verbose_name_plural = _('Sipariş Şablonu Kalemleri')
        unique_together = ['template', 'product']
    
    def __str__(self):
        return f"{self.template.name} - {self.product.name} x {self.quantity}"
