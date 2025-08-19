#!/usr/bin/env python
import os
import django

# Django ayarlarını yükle
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bakery_management.settings')
django.setup()

from inventory.models import Product, ProductCategory

print("=== SÜTLÜ TATLILAR GRUBU DÜZENLEMESİ ===")

# Hedef liste (görüntüdeki gibi)
target_products = [
    'SUPANGLE',
    'PROFİTEROL',  # Bu zaten silindi
    'MAGNOLYA ÇİLEKLİ',
    'MAGNOLYA OREOLU',
    'MAGNOLYA YABANMERSİNİ',
    'MAGNOLYA FISTIKLI',  # Bu KAHVELİ olarak değiştirildi
    'SÜTLAÇ'
]

print("\n📋 Hedef SÜTLÜ TATLILAR listesi:")
for product in target_products:
    print(f"  - {product}")

# Mevcut SÜTLÜ TATLILAR kategorisindeki ürünleri kontrol et
sutlu_category = ProductCategory.objects.get(name='SÜTLÜ TATLILAR')
current_products = Product.objects.filter(category=sutlu_category, is_active=True)

print(f"\n📊 Mevcut SÜTLÜ TATLILAR ({current_products.count()} adet):")
for product in current_products:
    print(f"  - {product.name}")

# SÜTLAÇ ürünü var mı kontrol et
sutlac_exists = Product.objects.filter(name='SÜTLAÇ', is_active=True).exists()
if not sutlac_exists:
    # SÜTLAÇ ürünü yoksa oluştur
    print(f"\n➕ SÜTLAÇ ürünü ekleniyor...")
    Product.objects.create(
        name='SÜTLAÇ',
        category=sutlu_category,
        unit='adet',
        price_per_unit=0.01,
        sku='SUTLU_009',
        is_active=True
    )
    print("✅ SÜTLAÇ ürünü eklendi")
else:
    print(f"\n✅ SÜTLAÇ ürünü zaten mevcut")

# Gereksiz ürünleri kontrol et ve temizle
print(f"\n🧹 Gereksiz ürünleri kontrol ediliyor...")

# MUZ SARMA DİLİM ve MUZLU SARMA DİLİM kontrolü (ikisi de var, biri yeterli)
muz_sarma_products = Product.objects.filter(
    category=sutlu_category, 
    name__icontains='MUZ',
    is_active=True
).filter(name__icontains='SARMA')

if muz_sarma_products.count() > 1:
    print(f"⚠️ Birden fazla MUZ SARMA ürünü bulundu:")
    for product in muz_sarma_products:
        print(f"  - {product.name}")
    
    # MUZLU SARMA DİLİM'i sil, MUZ SARMA DİLİM'i tut
    muzlu_sarma = Product.objects.filter(name='MUZLU SARMA DİLİM', is_active=True).first()
    if muzlu_sarma:
        muzlu_sarma.is_active = False
        muzlu_sarma.save()
        print(f"🗑️ {muzlu_sarma.name} silindi (duplikasyon)")

# Final kontrol
print(f"\n=== GÜNCEL SÜTLÜ TATLILAR LİSTESİ ===")
final_products = Product.objects.filter(category=sutlu_category, is_active=True).order_by('name')
print(f"\n📋 Güncel liste ({final_products.count()} adet):")
for product in final_products:
    print(f"  - {product.name}")

# Hedef listeyle karşılaştırma
print(f"\n🎯 Hedef listeyle karşılaştırma:")
current_names = [p.name for p in final_products]

for target in target_products:
    if target in current_names:
        print(f"  ✅ {target} - Mevcut")
    elif target == 'PROFİTEROL':
        print(f"  ✅ {target} - Silindi (istendiği gibi)")
    elif target == 'MAGNOLYA FISTIKLI':
        if 'MAGNOLYA KAHVELİ' in current_names:
            print(f"  ✅ {target} → MAGNOLYA KAHVELİ (değiştirildi)")
        else:
            print(f"  ❌ {target} - Eksik")
    else:
        print(f"  ❌ {target} - Eksik")

print(f"\n=== SÜTLÜ TATLILAR DÜZENLEMESİ TAMAMLANDI ===")
