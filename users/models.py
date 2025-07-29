from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Branch(models.Model):
    """Şube modeli - İmalat merkezi ve satış şubelerini temsil eder"""
    BRANCH_TYPE_CHOICES = [
        ('production', 'İmalat Merkezi'),
        ('sales', 'Satış Şubesi'),
    ]
    
    name = models.CharField(_('Şube Adı'), max_length=100)
    branch_type = models.CharField(_('Şube Tipi'), max_length=20, choices=BRANCH_TYPE_CHOICES)
    address = models.TextField(_('Adres'))
    phone = models.CharField(_('Telefon'), max_length=20)
    email = models.EmailField(_('E-posta'), blank=True, null=True)
    is_active = models.BooleanField(_('Aktif'), default=True)
    created_at = models.DateTimeField(_('Oluşturulma Tarihi'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Güncellenme Tarihi'), auto_now=True)
    
    class Meta:
        verbose_name = _('Şube')
        verbose_name_plural = _('Şubeler')
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_branch_type_display()})"


class CustomUser(AbstractUser):
    """Özel kullanıcı modeli - Rolleri ve şube atamasını içerir"""
    ROLE_CHOICES = [
        ('admin', 'Sistem Yöneticisi'),
        ('manager', 'Genel Müdür'),
        ('production_manager', 'İmalat Sorumlusu'),
        ('branch_manager', 'Şube Sorumlusu'),
        ('cashier', 'Kasiyer'),
        ('production_worker', 'İmalat Çalışanı'),
        ('delivery', 'Sevkiyat Sorumlusu'),
    ]
    
    role = models.CharField(
        _('Rol'),
        max_length=20,
        choices=ROLE_CHOICES,
        default='cashier'
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Şube'),
        related_name='users'
    )
    phone = models.CharField(_('Telefon'), max_length=20, blank=True)
    employee_id = models.CharField(_('Personel No'), max_length=20, unique=True, blank=True, null=True)
    is_active_employee = models.BooleanField(_('Aktif Personel'), default=True)
    hire_date = models.DateField(_('İşe Başlama Tarihi'), blank=True, null=True)
    created_at = models.DateTimeField(_('Oluşturulma Tarihi'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Güncellenme Tarihi'), auto_now=True)
    
    class Meta:
        verbose_name = _('Kullanıcı')
        verbose_name_plural = _('Kullanıcılar')
        ordering = ['username']
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
    
    def get_full_name(self):
        """Kullanıcının tam adını döndürür"""
        return f"{self.first_name} {self.last_name}".strip()
    
    def can_access_branch(self, branch):
        """Kullanıcının belirli bir şubeye erişim iznini kontrol eder"""
        if self.role in ['admin', 'manager']:
            return True
        return self.branch == branch
    
    def can_manage_orders(self):
        """Kullanıcının sipariş yönetimi yetkisini kontrol eder"""
        return self.role in ['admin', 'manager', 'branch_manager', 'production_manager']
    
    def can_manage_inventory(self):
        """Kullanıcının stok yönetimi yetkisini kontrol eder"""
        return self.role in ['admin', 'manager', 'branch_manager', 'production_manager']
    
    def can_manage_production(self):
        """Kullanıcının üretim yönetimi yetkisini kontrol eder"""
        return self.role in ['admin', 'manager', 'production_manager', 'production_worker']
    
    def can_view_reports(self):
        """Kullanıcının rapor görüntüleme yetkisini kontrol eder"""
        return self.role in ['admin', 'manager', 'branch_manager', 'production_manager']
    
    def can_manage_users(self):
        """Kullanıcının kullanıcı yönetimi yetkisini kontrol eder"""
        return self.role in ['admin', 'manager']


class UserProfile(models.Model):
    """Kullanıcı profil bilgileri - Ek bilgiler için"""
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('Kullanıcı')
    )
    avatar = models.ImageField(_('Profil Fotoğrafı'), upload_to='avatars/', blank=True, null=True)
    birth_date = models.DateField(_('Doğum Tarihi'), blank=True, null=True)
    address = models.TextField(_('Adres'), blank=True)
    emergency_contact = models.CharField(_('Acil Durum İletişim'), max_length=100, blank=True)
    emergency_phone = models.CharField(_('Acil Durum Telefon'), max_length=20, blank=True)
    notes = models.TextField(_('Notlar'), blank=True)
    created_at = models.DateTimeField(_('Oluşturulma Tarihi'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Güncellenme Tarihi'), auto_now=True)
    
    class Meta:
        verbose_name = _('Kullanıcı Profili')
        verbose_name_plural = _('Kullanıcı Profilleri')
    
    def __str__(self):
        return f"{self.user.get_full_name()} Profili"
