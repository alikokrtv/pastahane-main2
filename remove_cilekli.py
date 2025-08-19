#!/usr/bin/env python
import os
import django

# Django ayarlarını yükle
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bakery_management.settings')
django.setup()

from inventory.models import Product, ProductCategory

print("=== MAGNOLYA ÇİLEKLİ ÇIKARMA İŞLEMİ ===")

# MAGNOLYA ÇİLEKLİ'yi bul ve sil
magnolya_cilekli = Product.objects.filter(
    name='MAGNOLYA ÇİLEKLİ', 
    category__name='SÜTLÜ TATLILAR',
    is_active=True
).first()

if magnolya_cilekli:
    print(f"🔍 Bulunan ürün: {magnolya_cilekli.name}")
    print(f"   Kategori: {magnolya_cilekli.category.name}")
    print(f"   SKU: {magnolya_cilekli.sku}")
    
    # Ürünü pasif yap
    magnolya_cilekli.is_active = False
    magnolya_cilekli.save()
    print(f"✅ {magnolya_cilekli.name} SÜTLÜ TATLILAR grubundan çıkarıldı")
else:
    print("ℹ️ MAGNOLYA ÇİLEKLİ ürünü SÜTLÜ TATLILAR grubunda bulunamadı")

# Diğer kategorilerde MAGNOLYA ÇİLEKLİ var mı kontrol et
other_cilekli = Product.objects.filter(
    name__icontains='MAGNOLYA ÇİLEKLİ',
    is_active=True
).exclude(category__name='SÜTLÜ TATLILAR')

if other_cilekli.exists():
    print(f"\n🔍 Diğer kategorilerde bulunan MAGNOLYA ÇİLEKLİ ürünleri:")
    for product in other_cilekli:
        category_name = product.category.name if product.category else 'Kategori Yok'
        print(f"  - {product.name} (Kategori: {category_name})")
else:
    print(f"\nℹ️ Diğer kategorilerde MAGNOLYA ÇİLEKLİ ürünü bulunamadı")

print(f"\n=== GÜNCEL SÜTLÜ TATLILAR LİSTESİ ===")
sutlu_category = ProductCategory.objects.get(name='SÜTLÜ TATLILAR')
sutlu_products = Product.objects.filter(category=sutlu_category, is_active=True).order_by('name')

print(f"\n📋 Güncel SÜTLÜ TATLILAR ({sutlu_products.count()} adet):")
for product in sutlu_products:
    print(f"  - {product.name}")

# Hedef listeyle karşılaştırma (ÇİLEKLİ olmadan)
target_products = [
    'SUPANGLE',
    'MAGNOLYA OREOLU', 
    'MAGNOLYA YABANMERSİNİ',
    'MAGNOLYA KAHVELİ',  # FISTIKLI yerine
    'SÜTLAÇ'
]

print(f"\n🎯 Hedef liste (ÇİLEKLİ olmadan):")
current_names = [p.name for p in sutlu_products]

for target in target_products:
    if target in current_names:
        print(f"  ✅ {target} - Mevcut")
    else:
        print(f"  ❌ {target} - Eksik")

# Fazla ürünler var mı kontrol et
extra_products = [p for p in sutlu_products if p.name not in target_products]
if extra_products:
    print(f"\n⚠️ Fazla ürünler:")
    for product in extra_products:
        print(f"  - {product.name}")

print(f"\n=== MAGNOLYA ÇİLEKLİ ÇIKARMA İŞLEMİ TAMAMLANDI ===")
