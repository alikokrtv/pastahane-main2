from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta


User = get_user_model()


class ProductionPlan(models.Model):
    """Üretim planı"""
    STATUS_CHOICES = [
        ('draft', 'Taslak'),
        ('approved', 'Onaylandı'),
        ('in_progress', 'Devam Ediyor'),
        ('completed', 'Tamamlandı'),
        ('cancelled', 'İptal Edildi'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Düşük'),
        ('normal', 'Normal'),
        ('high', 'Yüksek'),
        ('urgent', 'Acil'),
    ]
    
    plan_number = models.CharField(_('Plan No'), max_length=50, unique=True)
    name = models.CharField(_('Plan Adı'), max_length=200)
    description = models.TextField(_('Açıklama'), blank=True)
    
    branch = models.ForeignKey(
        'users.Branch',
        on_delete=models.CASCADE,
        verbose_name=_('Üretim Merkezi'),
        related_name='production_plans'
    )
    
    status = models.CharField(_('Durum'), max_length=20, choices=STATUS_CHOICES, default='draft')
    priority = models.CharField(_('Öncelik'), max_length=10, choices=PRIORITY_CHOICES, default='normal')
    
    planned_start_date = models.DateField(_('Planlanan Başlangıç Tarihi'))
    planned_end_date = models.DateField(_('Planlanan Bitiş Tarihi'))
    actual_start_date = models.DateField(_('Gerçek Başlangıç Tarihi'), blank=True, null=True)
    actual_end_date = models.DateField(_('Gerçek Bitiş Tarihi'), blank=True, null=True)
    
    total_estimated_cost = models.DecimalField(
        _('Toplam Tahmini Maliyet'),
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00')
    )
    total_actual_cost = models.DecimalField(
        _('Toplam Gerçek Maliyet'),
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00')
    )
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Oluşturan'), related_name='created_production_plans')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Onaylayan'), related_name='approved_production_plans')
    approved_at = models.DateTimeField(_('Onaylanma Tarihi'), blank=True, null=True)
    
    created_at = models.DateTimeField(_('Oluşturulma Tarihi'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Güncellenme Tarihi'), auto_now=True)
    
    class Meta:
        verbose_name = _('Üretim Planı')
        verbose_name_plural = _('Üretim Planları')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['plan_number']),
            models.Index(fields=['status']),
            models.Index(fields=['planned_start_date']),
        ]
    
    def __str__(self):
        return f"{self.plan_number} - {self.name}"
    
    def save(self, *args, **kwargs):
        """Plan numarası otomatik oluştur"""
        if not self.plan_number:
            self.plan_number = self.generate_plan_number()
        super().save(*args, **kwargs)
    
    def generate_plan_number(self):
        """Plan numarası oluştur"""
        today = timezone.now().date()
        branch_code = self.branch.name[:3].upper() if self.branch else 'PRD'
        date_str = today.strftime('%Y%m%d')
        
        daily_count = ProductionPlan.objects.filter(
            branch=self.branch,
            created_at__date=today
        ).count() + 1
        
        return f"PLAN-{branch_code}-{date_str}-{daily_count:03d}"
    
    def get_completion_percentage(self):
        """Tamamlanma yüzdesini hesapla"""
        total_items = self.items.count()
        if total_items == 0:
            return 0
        
        completed_items = self.items.filter(status='completed').count()
        return (completed_items / total_items) * 100
    
    def is_overdue(self):
        """Plan gecikti mi?"""
        if self.status in ['completed', 'cancelled']:
            return False
        return timezone.now().date() > self.planned_end_date


class ProductionPlanItem(models.Model):
    """Üretim planı kalemleri"""
    production_plan = models.ForeignKey(
        ProductionPlan,
        on_delete=models.CASCADE,
        verbose_name=_('Üretim Planı'),
        related_name='items'
    )
    product = models.ForeignKey(
        'inventory.Product',
        on_delete=models.CASCADE,
        verbose_name=_('Ürün'),
        related_name='production_plan_items'
    )
    planned_quantity = models.DecimalField(
        _('Planlanan Miktar'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    produced_quantity = models.DecimalField(
        _('Üretilen Miktar'),
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    estimated_cost = models.DecimalField(
        _('Tahmini Maliyet'),
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )
    actual_cost = models.DecimalField(
        _('Gerçek Maliyet'),
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )
    notes = models.TextField(_('Notlar'), blank=True)
    
    class Meta:
        verbose_name = _('Üretim Planı Kalemi')
        verbose_name_plural = _('Üretim Planı Kalemleri')
        unique_together = ['production_plan', 'product']
    
    def __str__(self):
        return f"{self.production_plan.plan_number} - {self.product.name}"
    
    def get_completion_percentage(self):
        """Tamamlanma yüzdesini hesapla"""
        if self.planned_quantity > 0:
            return (self.produced_quantity / self.planned_quantity) * 100
        return 0
    
    def is_completed(self):
        """Tamamlandı mı?"""
        return self.produced_quantity >= self.planned_quantity


class ProductionBatch(models.Model):
    """Üretim partisi"""
    STATUS_CHOICES = [
        ('planned', 'Planlandı'),
        ('in_progress', 'Devam Ediyor'),
        ('quality_check', 'Kalite Kontrolde'),
        ('completed', 'Tamamlandı'),
        ('failed', 'Başarısız'),
        ('cancelled', 'İptal Edildi'),
    ]
    
    batch_number = models.CharField(_('Parti No'), max_length=50, unique=True)
    production_plan_item = models.ForeignKey(
        ProductionPlanItem,
        on_delete=models.CASCADE,
        verbose_name=_('Üretim Planı Kalemi'),
        related_name='batches'
    )
    
    recipe = models.ForeignKey(
        'inventory.Recipe',
        on_delete=models.CASCADE,
        verbose_name=_('Reçete'),
        related_name='production_batches'
    )
    
    planned_quantity = models.DecimalField(
        _('Planlanan Miktar'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    actual_quantity = models.DecimalField(
        _('Gerçek Miktar'),
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    waste_quantity = models.DecimalField(
        _('Fire Miktarı'),
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    status = models.CharField(_('Durum'), max_length=20, choices=STATUS_CHOICES, default='planned')
    
    # Zamanlama
    scheduled_start = models.DateTimeField(_('Planlanan Başlangıç'))
    scheduled_end = models.DateTimeField(_('Planlanan Bitiş'))
    actual_start = models.DateTimeField(_('Gerçek Başlangıç'), blank=True, null=True)
    actual_end = models.DateTimeField(_('Gerçek Bitiş'), blank=True, null=True)
    
    # Personel
    assigned_workers = models.ManyToManyField(
        User,
        verbose_name=_('Atanan Çalışanlar'),
        related_name='production_batches',
        blank=True
    )
    supervisor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Süpervizör'),
        related_name='supervised_batches'
    )
    
    # Maliyet
    material_cost = models.DecimalField(
        _('Malzeme Maliyeti'),
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )
    labor_cost = models.DecimalField(
        _('İşçilik Maliyeti'),
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )
    overhead_cost = models.DecimalField(
        _('Genel Gider'),
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )
    
    production_notes = models.TextField(_('Üretim Notları'), blank=True)
    quality_notes = models.TextField(_('Kalite Notları'), blank=True)
    
    created_at = models.DateTimeField(_('Oluşturulma Tarihi'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Güncellenme Tarihi'), auto_now=True)
    
    class Meta:
        verbose_name = _('Üretim Partisi')
        verbose_name_plural = _('Üretim Partileri')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['batch_number']),
            models.Index(fields=['status']),
            models.Index(fields=['scheduled_start']),
        ]
    
    def __str__(self):
        return f"{self.batch_number} - {self.recipe.product.name}"
    
    def save(self, *args, **kwargs):
        """Parti numarası otomatik oluştur"""
        if not self.batch_number:
            self.batch_number = self.generate_batch_number()
        super().save(*args, **kwargs)
    
    def generate_batch_number(self):
        """Parti numarası oluştur"""
        today = timezone.now().date()
        product_code = self.recipe.product.sku[:3] if self.recipe.product.sku else 'PRD'
        date_str = today.strftime('%Y%m%d')
        
        daily_count = ProductionBatch.objects.filter(
            created_at__date=today
        ).count() + 1
        
        return f"BATCH-{product_code}-{date_str}-{daily_count:03d}"
    
    def get_total_cost(self):
        """Toplam maliyeti hesapla"""
        return self.material_cost + self.labor_cost + self.overhead_cost
    
    def get_cost_per_unit(self):
        """Birim maliyeti hesapla"""
        if self.actual_quantity > 0:
            return self.get_total_cost() / self.actual_quantity
        return Decimal('0.00')
    
    def get_yield_percentage(self):
        """Verim yüzdesini hesapla"""
        if self.planned_quantity > 0:
            return (self.actual_quantity / self.planned_quantity) * 100
        return 0
    
    def get_duration(self):
        """Üretim süresini hesapla"""
        if self.actual_start and self.actual_end:
            return self.actual_end - self.actual_start
        return None
    
    def is_overdue(self):
        """Parti gecikti mi?"""
        if self.status in ['completed', 'failed', 'cancelled']:
            return False
        return timezone.now() > self.scheduled_end


class QualityCheck(models.Model):
    """Kalite kontrolü"""
    CHECK_TYPE_CHOICES = [
        ('raw_material', 'Hammadde Kontrolü'),
        ('in_process', 'Süreç İçi Kontrol'),
        ('final_product', 'Nihai Ürün Kontrolü'),
        ('packaging', 'Ambalaj Kontrolü'),
    ]
    
    RESULT_CHOICES = [
        ('pass', 'Geçti'),
        ('fail', 'Kaldı'),
        ('conditional', 'Şartlı Geçti'),
    ]
    
    batch = models.ForeignKey(
        ProductionBatch,
        on_delete=models.CASCADE,
        verbose_name=_('Üretim Partisi'),
        related_name='quality_checks'
    )
    
    check_type = models.CharField(_('Kontrol Tipi'), max_length=20, choices=CHECK_TYPE_CHOICES)
    check_date = models.DateTimeField(_('Kontrol Tarihi'), default=timezone.now)
    checked_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Kontrol Eden'))
    
    # Kontrol parametreleri
    temperature = models.DecimalField(
        _('Sıcaklık (°C)'),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )
    humidity = models.DecimalField(
        _('Nem (%)'),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    ph_level = models.DecimalField(
        _('pH Seviyesi'),
        max_digits=4,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(14)]
    )
    
    # Görsel kontrol
    appearance_score = models.IntegerField(
        _('Görünüm Puanı'),
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        blank=True,
        null=True
    )
    texture_score = models.IntegerField(
        _('Doku Puanı'),
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        blank=True,
        null=True
    )
    taste_score = models.IntegerField(
        _('Tat Puanı'),
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        blank=True,
        null=True
    )
    aroma_score = models.IntegerField(
        _('Aroma Puanı'),
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        blank=True,
        null=True
    )
    
    overall_result = models.CharField(_('Genel Sonuç'), max_length=20, choices=RESULT_CHOICES)
    notes = models.TextField(_('Notlar'), blank=True)
    corrective_actions = models.TextField(_('Düzeltici Eylemler'), blank=True)
    
    created_at = models.DateTimeField(_('Oluşturulma Tarihi'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Kalite Kontrolü')
        verbose_name_plural = _('Kalite Kontrolleri')
        ordering = ['-check_date']
    
    def __str__(self):
        return f"{self.batch.batch_number} - {self.get_check_type_display()} - {self.get_overall_result_display()}"
    
    def get_overall_score(self):
        """Genel puanı hesapla"""
        scores = [
            self.appearance_score,
            self.texture_score,
            self.taste_score,
            self.aroma_score
        ]
        valid_scores = [score for score in scores if score is not None]
        
        if valid_scores:
            return sum(valid_scores) / len(valid_scores)
        return None


class ProductionReport(models.Model):
    """Üretim raporu"""
    REPORT_TYPE_CHOICES = [
        ('daily', 'Günlük Rapor'),
        ('weekly', 'Haftalık Rapor'),
        ('monthly', 'Aylık Rapor'),
        ('batch', 'Parti Raporu'),
    ]
    
    report_number = models.CharField(_('Rapor No'), max_length=50, unique=True)
    report_type = models.CharField(_('Rapor Tipi'), max_length=20, choices=REPORT_TYPE_CHOICES)
    
    branch = models.ForeignKey(
        'users.Branch',
        on_delete=models.CASCADE,
        verbose_name=_('Şube'),
        related_name='production_reports'
    )
    
    report_date = models.DateField(_('Rapor Tarihi'), default=timezone.now)
    period_start = models.DateField(_('Dönem Başlangıcı'))
    period_end = models.DateField(_('Dönem Sonu'))
    
    # Üretim verileri
    total_batches = models.IntegerField(_('Toplam Parti Sayısı'), default=0)
    successful_batches = models.IntegerField(_('Başarılı Parti Sayısı'), default=0)
    failed_batches = models.IntegerField(_('Başarısız Parti Sayısı'), default=0)
    
    total_planned_quantity = models.DecimalField(
        _('Toplam Planlanan Miktar'),
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00')
    )
    total_produced_quantity = models.DecimalField(
        _('Toplam Üretilen Miktar'),
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00')
    )
    total_waste_quantity = models.DecimalField(
        _('Toplam Fire Miktarı'),
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00')
    )
    
    # Maliyet verileri
    total_material_cost = models.DecimalField(
        _('Toplam Malzeme Maliyeti'),
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00')
    )
    total_labor_cost = models.DecimalField(
        _('Toplam İşçilik Maliyeti'),
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00')
    )
    total_overhead_cost = models.DecimalField(
        _('Toplam Genel Gider'),
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00')
    )
    
    summary = models.TextField(_('Özet'), blank=True)
    recommendations = models.TextField(_('Öneriler'), blank=True)
    
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Oluşturan'))
    generated_at = models.DateTimeField(_('Oluşturulma Tarihi'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Üretim Raporu')
        verbose_name_plural = _('Üretim Raporları')
        ordering = ['-generated_at']
        indexes = [
            models.Index(fields=['report_number']),
            models.Index(fields=['report_type']),
            models.Index(fields=['report_date']),
        ]
    
    def __str__(self):
        return f"{self.report_number} - {self.get_report_type_display()}"
    
    def save(self, *args, **kwargs):
        """Rapor numarası otomatik oluştur"""
        if not self.report_number:
            self.report_number = self.generate_report_number()
        super().save(*args, **kwargs)
    
    def generate_report_number(self):
        """Rapor numarası oluştur"""
        today = timezone.now().date()
        type_code = self.report_type.upper()[:3]
        date_str = today.strftime('%Y%m%d')
        
        daily_count = ProductionReport.objects.filter(
            report_type=self.report_type,
            generated_at__date=today
        ).count() + 1
        
        return f"RPT-{type_code}-{date_str}-{daily_count:03d}"
    
    def get_success_rate(self):
        """Başarı oranını hesapla"""
        if self.total_batches > 0:
            return (self.successful_batches / self.total_batches) * 100
        return 0
    
    def get_yield_rate(self):
        """Verim oranını hesapla"""
        if self.total_planned_quantity > 0:
            return (self.total_produced_quantity / self.total_planned_quantity) * 100
        return 0
    
    def get_waste_rate(self):
        """Fire oranını hesapla"""
        if self.total_produced_quantity > 0:
            return (self.total_waste_quantity / self.total_produced_quantity) * 100
        return 0
    
    def get_total_cost(self):
        """Toplam maliyeti hesapla"""
        return self.total_material_cost + self.total_labor_cost + self.total_overhead_cost
    
    def get_cost_per_unit(self):
        """Birim maliyeti hesapla"""
        if self.total_produced_quantity > 0:
            return self.get_total_cost() / self.total_produced_quantity
        return Decimal('0.00')
