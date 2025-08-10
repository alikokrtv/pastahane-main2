#!/usr/bin/env python
import os
import django

# Django ayarlarını yükle
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bakery_management.settings')
django.setup()

from inventory.models import Product

print("=== SPESYAL ÜRÜNLER DÜZELTMELERİ ===")

# 1. İzmir Bomba birimini tepsi'den adet'e değiştir
izmir_bomba = Product.objects.filter(name__icontains='İZMİR BOMBA', is_active=True).first()
if izmir_bomba:
    old_unit = izmir_bomba.unit
    izmir_bomba.unit = 'adet'
    izmir_bomba.save()
    print(f"✅ {izmir_bomba.name}: {old_unit} → adet")
else:
    print("❌ İzmir Bomba ürünü bulunamadı")

# 2. Ganaj yazım hatalarını düzelt (canaj → ganaj)
canaj_products = Product.objects.filter(name__icontains='CANAJ', is_active=True)
for product in canaj_products:
    old_name = product.name
    new_name = product.name.replace('CANAJ', 'GANAJ').replace('canaj', 'ganaj')
    product.name = new_name
    product.save()
    print(f"✅ Yazım düzeltmesi: {old_name} → {new_name}")

if not canaj_products.exists():
    print("ℹ️ 'CANAJ' içeren ürün bulunamadı")

# 3. Tüm ürünlerde ganaj yazım kontrolü
all_products = Product.objects.filter(is_active=True)
ganaj_count = 0
for product in all_products:
    if 'canaj' in product.name.lower():
        old_name = product.name
        new_name = product.name.replace('CANAJ', 'GANAJ').replace('canaj', 'ganaj').replace('Canaj', 'Ganaj')
        product.name = new_name
        product.save()
        print(f"✅ Genel düzeltme: {old_name} → {new_name}")
        ganaj_count += 1

if ganaj_count == 0:
    print("ℹ️ Düzeltilecek ganaj yazımı bulunamadı")

print("\n=== GÜNCEL SPESYAL ÜRÜNLER ===")
spesyal_products = Product.objects.filter(category__name='SPESYAL ÜRÜNLER', is_active=True)
for p in spesyal_products:
    print(f"- {p.name} ({p.unit}) - SKU: {p.sku}")

print("\n=== DÜZELTMELER TAMAMLANDI ===")
