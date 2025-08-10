#!/usr/bin/env python
import os
import django

# Django ayarlarını yükle
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bakery_management.settings')
django.setup()

from inventory.models import Product

print("=== PORTALLI → PORTAKALLI DÜZELTMESİ ===")

# PORTALLI ürünlerini bul ve PORTAKALLI olarak değiştir
portalli_products = Product.objects.filter(name__icontains='PORTALLI', is_active=True)

if portalli_products.exists():
    print(f"\n🔍 Bulunan PORTALLI ürünleri ({portalli_products.count()} adet):")
    
    for product in portalli_products:
        old_name = product.name
        new_name = product.name.replace('PORTALLI', 'PORTAKALLI').replace('portalli', 'portakalli')
        product.name = new_name
        product.save()
        print(f"  ✅ {old_name} → {new_name}")
    
    print(f"\n✅ {portalli_products.count()} ürün başarıyla düzeltildi")
else:
    print("\nℹ️ PORTALLI ürünü bulunamadı")

# Kontrol: PORTAKALLI ürünlerini listele
print("\n=== PORTAKALLI ÜRÜNLERİ KONTROLÜ ===")
portakalli_products = Product.objects.filter(name__icontains='PORTAKALLI', is_active=True)

if portakalli_products.exists():
    print(f"\n📋 Mevcut PORTAKALLI ürünleri ({portakalli_products.count()} adet):")
    for product in portakalli_products:
        category_name = product.category.name if product.category else 'Kategori Yok'
        print(f"  - {product.name} (Kategori: {category_name}) (SKU: {product.sku})")
else:
    print("\nℹ️ PORTAKALLI ürünü bulunamadı")

print("\n=== EKLER ÇEŞİTLERİ LİSTESİ ===")
ekler_products = Product.objects.filter(category__name='EKLER ÇEŞİTLERİ', is_active=True).order_by('name')
print(f"\n📋 Güncel EKLER ÇEŞİTLERİ ({ekler_products.count()} adet):")
for product in ekler_products:
    print(f"  - {product.name}")

print("\n=== DÜZELTME TAMAMLANDI ===")
