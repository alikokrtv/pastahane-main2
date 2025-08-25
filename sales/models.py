from django.db import models


class Satislar(models.Model):
    id = models.BigAutoField(primary_key=True)
    fisno = models.CharField(max_length=50, db_index=True)
    tarih = models.DateTimeField(null=True, blank=True)
    musteriadi = models.CharField(max_length=255, null=True, blank=True)
    urun = models.CharField(max_length=255, null=True, blank=True)
    adet = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    fiyat = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    toplam = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    kar = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    odemesi = models.CharField(max_length=50, null=True, blank=True)
    satisiyapan = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        managed = False  # Var olan tablo
        db_table = "satislar"

    def __str__(self):
        return f"{self.fisno} - {self.urun} ({self.adet})"
