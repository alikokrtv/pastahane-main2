#!/usr/bin/env python
import os
import django

# Django ayarlarını yükle
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bakery_management.settings')
django.setup()

from inventory.models import Product, ProductCategory

print("=== ÜRÜN GÜNCELLEMELERİ BAŞLIYOR ===")

# 1. SİLİNECEK ÜRÜNLER
print("\n1. SİLİNECEK ÜRÜNLER:")

# MALAGA BEYAZ ve MALAGA SİYAH (zaten yok)
malaga_beyaz = Product.objects.filter(name__icontains='MALAGA BEYAZ', is_active=True)
malaga_beyaz.update(is_active=False)
print(f"- MALAGA BEYAZ: {malaga_beyaz.count()} ürün silindi")

malaga_siyah = Product.objects.filter(name__icontains='MALAGA SİYAH', is_active=True)
malaga_siyah.update(is_active=False)
print(f"- MALAGA SİYAH: {malaga_siyah.count()} ürün silindi")

# PROFİTEROLLÜ pastalar
profiterol_pasta = Product.objects.filter(name__icontains='PROFİTEROLLÜ', is_active=True)
for p in profiterol_pasta:
    print(f"  - {p.name} silindi")
    p.is_active = False
    p.save()

# PROFİTEROL (sütlü tatlı)
profiterol_sutlu = Product.objects.filter(name='PROFİTEROL', is_active=True)
for p in profiterol_sutlu:
    print(f"  - {p.name} silindi")
    p.is_active = False
    p.save()

# REDVELET pastalar
redvelet_products = Product.objects.filter(name__icontains='REDVELET', is_active=True)
for p in redvelet_products:
    print(f"  - {p.name} silindi")
    p.is_active = False
    p.save()

# FISTIKLI pastalar (FISTIKLI BEYAZ ve FISTIKLI SİYAH)
fistikli_pasta = Product.objects.filter(name__icontains='FISTIKLI', category__name='PASTA ÇEŞİTLERİ', is_active=True)
for p in fistikli_pasta:
    print(f"  - {p.name} silindi")
    p.is_active = False
    p.save()

# EKLER FISTIKLI -> EKLER KAHVELİ olarak değiştir
ekler_fistikli = Product.objects.filter(name='EKLER FISTIKLI', is_active=True).first()
if ekler_fistikli:
    ekler_fistikli.name = 'EKLER KAHVELİ'
    ekler_fistikli.save()
    print(f"  - EKLER FISTIKLI -> EKLER KAHVELİ olarak değiştirildi")

# MAGNOLYA FISTIKLI -> MAGNOLYA KAHVELİ olarak değiştir
magnolya_fistikli = Product.objects.filter(name='MAGNOLYA FISTIKLI', is_active=True).first()
if magnolya_fistikli:
    magnolya_fistikli.name = 'MAGNOLYA KAHVELİ'
    magnolya_fistikli.save()
    print(f"  - MAGNOLYA FISTIKLI -> MAGNOLYA KAHVELİ olarak değiştirildi")

print("\n2. EKLENECEK ÜRÜNLER:")

# Kategorileri al
pasta_category = ProductCategory.objects.get(name='PASTA ÇEŞİTLERİ')
sutlu_category = ProductCategory.objects.get(name='SÜTLÜ TATLILAR')
ekler_category = ProductCategory.objects.get(name='EKLER ÇEŞİTLERİ')

# ÇİKOLATA MİX pastalar ekle
cikolata_mix_data = [
    ('K4', 'PASTA_301_K4'),
    ('No0', 'PASTA_302_No0'),
    ('No1', 'PASTA_303_No1'),
    ('No2', 'PASTA_304_No2')
]
for size, sku in cikolata_mix_data:
    product_name = f'ÇİKOLATA MİX - {size}'
    if not Product.objects.filter(name=product_name).exists():
        Product.objects.create(
            name=product_name,
            category=pasta_category,
            unit='adet',
            price_per_unit=0.01,
            sku=sku,
            is_active=True
        )
        print(f"  + {product_name} eklendi (SKU: {sku})")

# REDVEL MİX pastalar ekle
redvel_mix_data = [
    ('K4', 'PASTA_305_K4'),
    ('No0', 'PASTA_306_No0'),
    ('No1', 'PASTA_307_No1'),
    ('No2', 'PASTA_308_No2')
]
for size, sku in redvel_mix_data:
    product_name = f'REDVEL MİX - {size}'
    if not Product.objects.filter(name=product_name).exists():
        Product.objects.create(
            name=product_name,
            category=pasta_category,
            unit='adet',
            price_per_unit=0.01,
            sku=sku,
            is_active=True
        )
        print(f"  + {product_name} eklendi (SKU: {sku})")

# MUZ SARMA DİLİM (sütlü tatlılar grubuna adet olarak)
if not Product.objects.filter(name='MUZ SARMA DİLİM').exists():
    Product.objects.create(
        name='MUZ SARMA DİLİM',
        category=sutlu_category,
        unit='adet',
        price_per_unit=0.01,
        sku='SUTLU_008',
        is_active=True
    )
    print(f"  + MUZ SARMA DİLİM eklendi (SÜTLÜ TATLILAR) (SKU: SUTLU_008)")

# EKLER ÇİLEKLİ BEYAZ ekle (eğer yoksa)
if not Product.objects.filter(name='EKLER ÇİLEKLİ BEYAZ').exists():
    Product.objects.create(
        name='EKLER ÇİLEKLİ BEYAZ',
        category=ekler_category,
        unit='tepsi',
        price_per_unit=0.01,
        sku='EKLER_012',
        is_active=True
    )
    print(f"  + EKLER ÇİLEKLİ BEYAZ eklendi (SKU: EKLER_012)")

print("\n=== GÜNCELLEMELER TAMAMLANDI ===")

# Kontrol listesi
print("\n=== KONTROL LİSTESİ ===")
print("\nSÜTLÜ TATLILAR:")
sutlu_products = Product.objects.filter(category__name='SÜTLÜ TATLILAR', is_active=True)
for p in sutlu_products:
    print(f"  - {p.name}")

print("\nEKLER ÇEŞİTLERİ:")
ekler_products = Product.objects.filter(category__name='EKLER ÇEŞİTLERİ', is_active=True)
for p in ekler_products:
    print(f"  - {p.name}")

print("\nYENİ PASTA ÇEŞİTLERİ (ÇİKOLATA MİX ve REDVEL MİX):")
new_pastas = Product.objects.filter(
    category__name='PASTA ÇEŞİTLERİ', 
    name__icontains='MİX', 
    is_active=True
)
for p in new_pastas:
    print(f"  - {p.name}")
