from django.db import models


class Satislar(models.Model):
    id = models.BigAutoField(primary_key=True)
    fisno = models.CharField(max_length=50, db_index=True)
    tarih = models.DateTimeField(null=True)
    musterikod = models.CharField(max_length=50, null=True, blank=True)
    fiyat = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    adet = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    toplam = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    kar = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    musteriadi = models.CharField(max_length=255, null=True, blank=True)
    urun = models.CharField(max_length=255, null=True, blank=True)
    grub = models.CharField(max_length=100, null=True, blank=True)
    odemesi = models.CharField(max_length=50, null=True, blank=True)
    satisiyapan = models.CharField(max_length=100, null=True, blank=True)
    barkod = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        managed = False  # mevcut tabloya müdahale etmez
        db_table = "satislar"
