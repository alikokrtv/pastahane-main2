from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from decimal import Decimal


User = get_user_model()


class ProductCategory(models.Model):
    """Ürün kategorileri"""
    name = models.CharField(_('Kategori Adı'), max_length=100)
    description = models.TextField(_('Açıklama'), blank=True)
    is_active = models.BooleanField(_('Aktif'), default=True)
    created_at = models.DateTimeField(_('Oluşturulma Tarihi'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Güncellenme Tarihi'), auto_now=True)
    
    class Meta:
        verbose_name = _('Ürün Kategorisi')
        verbose_name_plural = _('Ürün Kategorileri')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Ürün modeli"""
    UNIT_CHOICES = [
        ('kg', 'Kilogram'),
        ('adet', 'Adet'),
        ('porsiyon', 'Porsiyon'),
        ('litre', 'Litre'),
        ('gram', 'Gram'),
        ('paket', 'Paket'),
    ]
    
    name = models.CharField(_('Ürün Adı'), max_length=200)
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        verbose_name=_('Kategori'),
        related_name='products'
    )
    description = models.TextField(_('Açıklama'), blank=True)
    unit = models.CharField(_('Birim'), max_length=20, choices=UNIT_CHOICES, default='adet')
    price_per_unit = models.DecimalField(
        _('Birim Fiyat'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    cost_per_unit = models.DecimalField(
        _('Birim Maliyet'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        default=Decimal('0.00')
    )
    barcode = models.CharField(_('Barkod'), max_length=50, blank=True, unique=True, null=True)
    sku = models.CharField(_('Stok Kodu'), max_length=50, unique=True)
    is_active = models.BooleanField(_('Aktif'), default=True)
    is_produced = models.BooleanField(_('Üretiliyor'), default=True, help_text='Bu ürün kendi üretimimiz mi?')
    shelf_life_days = models.IntegerField(_('Raf Ömrü (Gün)'), default=7, help_text='Ürünün raf ömrü')
    created_at = models.DateTimeField(_('Oluşturulma Tarihi'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Güncellenme Tarihi'), auto_now=True)
    
    class Meta:
        verbose_name = _('Ürün')
        verbose_name_plural = _('Ürünler')
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_unit_display()})"
    
    def get_profit_margin(self):
        """Kar marjını hesaplar"""
        if self.cost_per_unit > 0:
            return ((self.price_per_unit - self.cost_per_unit) / self.price_per_unit) * 100
        return 0


class Recipe(models.Model):
    """Reçete modeli - Ürün üretimi için gerekli malzemeler"""
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('Ürün'),
        related_name='recipe'
    )
    name = models.CharField(_('Reçete Adı'), max_length=200)
    description = models.TextField(_('Açıklama'), blank=True)
    yield_quantity = models.DecimalField(
        _('Çıkan Miktar'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text='Bu reçeteden kaç birim ürün çıkar'
    )
    preparation_time = models.IntegerField(_('Hazırlık Süresi (dakika)'), default=0)
    cooking_time = models.IntegerField(_('Pişirme Süresi (dakika)'), default=0)
    instructions = models.TextField(_('Yapılış Talimatları'), blank=True)
    is_active = models.BooleanField(_('Aktif'), default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=_('Oluşturan'))
    created_at = models.DateTimeField(_('Oluşturulma Tarihi'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Güncellenme Tarihi'), auto_now=True)
    
    class Meta:
        verbose_name = _('Reçete')
        verbose_name_plural = _('Reçeteler')
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.product.name}"
    
    def get_total_cost(self):
        """Reçetenin toplam maliyetini hesaplar"""
        total_cost = sum(
            ingredient.quantity * ingredient.ingredient.cost_per_unit
            for ingredient in self.ingredients.all()
        )
        return total_cost
    
    def get_cost_per_unit(self):
        """Birim maliyeti hesaplar"""
        total_cost = self.get_total_cost()
        if self.yield_quantity > 0:
            return total_cost / self.yield_quantity
        return 0


class RecipeIngredient(models.Model):
    """Reçete malzemeleri"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name=_('Reçete'),
        related_name='ingredients'
    )
    ingredient = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('Malzeme'),
        related_name='used_in_recipes'
    )
    quantity = models.DecimalField(
        _('Miktar'),
        max_digits=10,
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.001'))]
    )
    unit = models.CharField(_('Birim'), max_length=20, choices=Product.UNIT_CHOICES)
    notes = models.CharField(_('Notlar'), max_length=200, blank=True)
    created_at = models.DateTimeField(_('Oluşturulma Tarihi'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Reçete Malzemesi')
        verbose_name_plural = _('Reçete Malzemeleri')
        unique_together = ['recipe', 'ingredient']
    
    def __str__(self):
        return f"{self.recipe.name} - {self.ingredient.name} ({self.quantity} {self.get_unit_display()})"
    
    def get_cost(self):
        """Bu malzemenin toplam maliyetini hesaplar"""
        return self.quantity * self.ingredient.cost_per_unit


class Inventory(models.Model):
    """Stok takibi"""
    branch = models.ForeignKey(
        'users.Branch',
        on_delete=models.CASCADE,
        verbose_name=_('Şube'),
        related_name='inventory'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('Ürün'),
        related_name='inventory'
    )
    quantity = models.DecimalField(
        _('Mevcut Miktar'),
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    reserved_quantity = models.DecimalField(
        _('Rezerve Miktar'),
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text='Siparişler için rezerve edilen miktar'
    )
    minimum_stock = models.DecimalField(
        _('Minimum Stok'),
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    maximum_stock = models.DecimalField(
        _('Maksimum Stok'),
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    last_updated = models.DateTimeField(_('Son Güncelleme'), auto_now=True)
    last_updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=_('Güncelleyen'))
    
    class Meta:
        verbose_name = _('Stok')
        verbose_name_plural = _('Stoklar')
        unique_together = ['branch', 'product']
        ordering = ['branch', 'product']
    
    def __str__(self):
        return f"{self.branch.name} - {self.product.name}: {self.quantity} {self.product.get_unit_display()}"
    
    def get_available_quantity(self):
        """Mevcut kullanılabilir miktarı döndürür"""
        return self.quantity - self.reserved_quantity
    
    def is_low_stock(self):
        """Stok seviyesi düşük mü?"""
        return self.quantity <= self.minimum_stock
    
    def is_out_of_stock(self):
        """Stok tükendi mi?"""
        return self.quantity <= 0
    
    def can_fulfill_order(self, requested_quantity):
        """Belirtilen miktar için stok yeterli mi?"""
        return self.get_available_quantity() >= requested_quantity


class StockMovement(models.Model):
    """Stok hareketi - Giriş/Çıkış kayıtları"""
    MOVEMENT_TYPE_CHOICES = [
        ('in', 'Giriş'),
        ('out', 'Çıkış'),
        ('transfer', 'Transfer'),
        ('production', 'Üretim'),
        ('sale', 'Satış'),
        ('waste', 'İmha'),
        ('adjustment', 'Düzeltme'),
    ]
    
    inventory = models.ForeignKey(
        Inventory,
        on_delete=models.CASCADE,
        verbose_name=_('Stok'),
        related_name='movements'
    )
    movement_type = models.CharField(_('Hareket Tipi'), max_length=20, choices=MOVEMENT_TYPE_CHOICES)
    quantity = models.DecimalField(
        _('Miktar'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    reference_number = models.CharField(_('Referans No'), max_length=50, blank=True)
    notes = models.TextField(_('Notlar'), blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Oluşturan'))
    created_at = models.DateTimeField(_('Oluşturulma Tarihi'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Stok Hareketi')
        verbose_name_plural = _('Stok Hareketleri')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.inventory.product.name} - {self.get_movement_type_display()}: {self.quantity}"
    
    def save(self, *args, **kwargs):
        """Stok hareketi kayıtlarken inventory miktarını günceller"""
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            # Yeni hareket kaydedildiğinde stok miktarını güncelle
            if self.movement_type in ['in', 'production']:
                self.inventory.quantity += self.quantity
            elif self.movement_type in ['out', 'sale', 'waste']:
                self.inventory.quantity -= self.quantity
            elif self.movement_type == 'adjustment':
                # Düzeltme için quantity pozitif veya negatif olabilir
                self.inventory.quantity += self.quantity
            
            self.inventory.last_updated_by = self.created_by
            self.inventory.save()


class WasteRecord(models.Model):
    """İmha kayıtları"""
    WASTE_REASON_CHOICES = [
        ('expired', 'Son Kullanma Tarihi Geçmiş'),
        ('damaged', 'Hasar'),
        ('quality', 'Kalite Sorunu'),
        ('overproduction', 'Aşırı Üretim'),
        ('customer_return', 'Müşteri İadesi'),
        ('other', 'Diğer'),
    ]
    
    inventory = models.ForeignKey(
        Inventory,
        on_delete=models.CASCADE,
        verbose_name=_('Stok'),
        related_name='waste_records'
    )
    quantity = models.DecimalField(
        _('İmha Miktarı'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    reason = models.CharField(_('İmha Sebebi'), max_length=20, choices=WASTE_REASON_CHOICES)
    description = models.TextField(_('Açıklama'), blank=True)
    cost_impact = models.DecimalField(
        _('Maliyet Etkisi'),
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text='İmha edilen ürünün maliyet değeri'
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Oluşturan'))
    created_at = models.DateTimeField(_('İmha Tarihi'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('İmha Kaydı')
        verbose_name_plural = _('İmha Kayıtları')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.inventory.product.name} - {self.quantity} - {self.get_reason_display()}"
    
    def save(self, *args, **kwargs):
        """İmha kaydı oluştururken maliyet etkisini hesapla"""
        self.cost_impact = self.quantity * self.inventory.product.cost_per_unit
        super().save(*args, **kwargs)
        
        # Stok hareketini otomatik oluştur
        StockMovement.objects.create(
            inventory=self.inventory,
            movement_type='waste',
            quantity=self.quantity,
            reference_number=f'WASTE-{self.id}',
            notes=f'İmha - {self.get_reason_display()}: {self.description}',
            created_by=self.created_by
        )
