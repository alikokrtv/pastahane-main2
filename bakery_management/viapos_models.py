# ViaPos MySQL tabloları için Django modelleri
from django.db import models
from decimal import Decimal

class ViaposStok(models.Model):
    """ViaPos stok tablosu modeli"""
    id = models.AutoField(primary_key=True)
    tur = models.CharField(max_length=50, null=True, blank=True)
    anastokkodu = models.DecimalField(max_digits=18, decimal_places=0, null=True, blank=True)
    stokkodu = models.DecimalField(max_digits=18, decimal_places=0, null=True, blank=True)
    barkod = models.CharField(max_length=250, null=True, blank=True)
    stokadi = models.CharField(max_length=250, null=True, blank=True)
    alis = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    satis = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    satis1 = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    satis2 = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    satis3 = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    satis4 = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    satis5 = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    aliskdv = models.DecimalField(max_digits=18, decimal_places=0, null=True, blank=True)
    satiskdv = models.DecimalField(max_digits=18, decimal_places=0, null=True, blank=True)
    birim = models.CharField(max_length=50, null=True, blank=True)
    birimcarpani = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    ulke = models.CharField(max_length=50, null=True, blank=True)
    rafomru = models.DecimalField(max_digits=18, decimal_places=0, null=True, blank=True)
    kritikstok = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    hedefstok = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    grami = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    puan = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    aciklama = models.CharField(max_length=500, null=True, blank=True)
    yazici = models.CharField(max_length=50, null=True, blank=True)
    seritakip = models.CharField(max_length=1, null=True, blank=True)
    etiketyaz = models.CharField(max_length=1, null=True, blank=True)
    aktif = models.CharField(max_length=1, null=True, blank=True)
    onlineterazi = models.CharField(max_length=1, null=True, blank=True)
    barkodluterazi = models.CharField(max_length=1, null=True, blank=True)
    kayitedenkodu = models.CharField(max_length=50, null=True, blank=True)
    kayittarihi = models.DateTimeField(null=True, blank=True)
    duzenleyenkodu = models.CharField(max_length=50, null=True, blank=True)
    duzenlemetarihi = models.DateTimeField(null=True, blank=True)
    silenkodu = models.CharField(max_length=50, null=True, blank=True)
    silmetarihi = models.DateTimeField(null=True, blank=True)
    sonfiyatdegisimtarihi = models.DateTimeField(null=True, blank=True)
    renk = models.CharField(max_length=50, null=True, blank=True)
    beden = models.CharField(max_length=50, null=True, blank=True)
    lot = models.CharField(max_length=50, null=True, blank=True)
    raf = models.CharField(max_length=50, null=True, blank=True)
    sira = models.CharField(max_length=50, null=True, blank=True)
    grup1 = models.CharField(max_length=50, null=True, blank=True)
    grup2 = models.CharField(max_length=50, null=True, blank=True)
    grup3 = models.CharField(max_length=50, null=True, blank=True)
    grup4 = models.CharField(max_length=50, null=True, blank=True)
    grup5 = models.CharField(max_length=50, null=True, blank=True)
    kolibarkod = models.CharField(max_length=50, null=True, blank=True)
    koliadedi = models.CharField(max_length=50, null=True, blank=True)
    parabirimi = models.CharField(max_length=50, null=True, blank=True)
    konum = models.CharField(max_length=50, null=True, blank=True)
    konumkodu = models.DecimalField(max_digits=18, decimal_places=0, null=True, blank=True)

    class Meta:
        managed = False  # Django bu tabloyu yönetmez, sadece okur
        db_table = 'stok'
        app_label = 'viapos'

    def __str__(self):
        return f"{self.stokadi} ({self.stokkodu})"

    @property
    def is_pasta(self):
        """Pasta ürünü olup olmadığını kontrol eder"""
        if not self.stokadi:
            return False
        
        pasta_keywords = [
            'pasta', 'turta', 'kek', 'tart', 'dilim', 'yaş pasta',
            'doğum günü', 'nikah', 'nişan', 'sünnet', 'çikolatalı',
            'meyveli', 'kremalı', 'mousse', 'tiramisu', 'cheesecake'
        ]
        
        stok_adi_lower = self.stokadi.lower()
        return any(keyword in stok_adi_lower for keyword in pasta_keywords)

    @property
    def pasta_category(self):
        """Pasta kategorisini belirler"""
        if not self.is_pasta:
            return "Diğer"
        
        stok_adi_lower = self.stokadi.lower() if self.stokadi else ""
        
        if any(word in stok_adi_lower for word in ['dilim', 'parça']):
            return "Dilim Pastalar"
        elif any(word in stok_adi_lower for word in ['turta', 'büyük', 'tam']):
            return "Turta Pastalar"
        elif any(word in stok_adi_lower for word in ['kek', 'sade']):
            return "Kekler"
        elif any(word in stok_adi_lower for word in ['özel', 'tasarım']):
            return "Özel Pastalar"
        else:
            return "Diğer Pastalar"


class ViaposHareket(models.Model):
    """ViaPos hareket tablosu modeli"""
    id = models.AutoField(primary_key=True)
    tur = models.CharField(max_length=50, null=True, blank=True)
    turkodu = models.DecimalField(max_digits=18, decimal_places=0, null=True, blank=True)
    islem = models.CharField(max_length=50, null=True, blank=True)
    islemgrup = models.CharField(max_length=50, null=True, blank=True)
    hareketkodu = models.DecimalField(max_digits=18, decimal_places=0, null=True, blank=True)
    firmakodu = models.DecimalField(max_digits=18, decimal_places=0, null=True, blank=True)
    firmaadi = models.CharField(max_length=250, null=True, blank=True)
    kasakodu = models.DecimalField(max_digits=18, decimal_places=0, null=True, blank=True)
    kasaadi = models.CharField(max_length=250, null=True, blank=True)
    faturano = models.CharField(max_length=50, null=True, blank=True)
    hareketnotu = models.CharField(max_length=500, null=True, blank=True)
    sube = models.CharField(max_length=50, null=True, blank=True)
    subeadi = models.CharField(max_length=50, null=True, blank=True)
    subealan = models.CharField(max_length=50, null=True, blank=True)
    subeadialan = models.CharField(max_length=50, null=True, blank=True)
    aktif = models.CharField(max_length=1, null=True, blank=True)
    kayitedenkodu = models.CharField(max_length=50, null=True, blank=True)
    kayittarihi = models.DateTimeField(null=True, blank=True)
    duzenleyenkodu = models.CharField(max_length=50, null=True, blank=True)
    duzenlemetarihi = models.DateTimeField(null=True, blank=True)
    silenkodu = models.CharField(max_length=50, null=True, blank=True)
    silmetarihi = models.DateTimeField(null=True, blank=True)
    virmanturu = models.DecimalField(max_digits=18, decimal_places=0, null=True, blank=True)
    virmankodu = models.DecimalField(max_digits=18, decimal_places=0, null=True, blank=True)
    kdvtoplam = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    aratoplam = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    indirim = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    toplam = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    kasatoplam = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    kar = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    parabirimi = models.CharField(max_length=50, null=True, blank=True)
    parakur = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    resmiyet = models.CharField(max_length=50, null=True, blank=True)
    konum = models.CharField(max_length=50, null=True, blank=True)
    konumkodu = models.DecimalField(max_digits=18, decimal_places=0, null=True, blank=True)

    class Meta:
        managed = False  # Django bu tabloyu yönetmez, sadece okur
        db_table = 'hareket'
        app_label = 'viapos'

    def __str__(self):
        return f"Hareket {self.hareketkodu} - {self.islem}"
