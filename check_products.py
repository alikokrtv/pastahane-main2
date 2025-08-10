#!/usr/bin/env python
import os
import django

# Django ayarlarını yükle
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bakery_management.settings')
django.setup()

from inventory.models import Product, ProductCategory

print("=== MEVCUT KATEGORİLER ===")
for cat in ProductCategory.objects.all():
    count = Product.objects.filter(category=cat, is_active=True).count()
    print(f"{cat.name}: {count} ürün")

print("\n=== SÜTLÜ TATLILAR ===")
sutlu_products = Product.objects.filter(category__name='SÜTLÜ TATLILAR', is_active=True)
for p in sutlu_products:
    print(f"- {p.name}")

print("\n=== EKLER ÇEŞİTLERİ ===")
ekler_products = Product.objects.filter(category__name='EKLER ÇEŞİTLERİ', is_active=True)
for p in ekler_products:
    print(f"- {p.name}")

print("\n=== TEPSİLİ ÜRÜNLER ===")
tepsili_products = Product.objects.filter(category__name='TEPSİLİ ÜRÜNLER', is_active=True)
for p in tepsili_products:
    print(f"- {p.name}")

print("\n=== SİLİNECEK ÜRÜNLER (KONTROL) ===")
silinecek_urunler = ['MALAGA BEYAZ', 'MALAGA SİYAH', 'PROFİTEROLLU', 'REDVELET', 'FISTIKLI']
for urun_adi in silinecek_urunler:
    products = Product.objects.filter(name__icontains=urun_adi, is_active=True)
    if products:
        for p in products:
            print(f"- BULUNDU: {p.name} (ID: {p.id})")
    else:
        print(f"- BULUNAMADI: {urun_adi}")
