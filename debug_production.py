#!/usr/bin/env python
import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bakery_management.settings')
django.setup()

from inventory.models import Product, ProductCategory

print("=== PRODUCTION DEBUG ===")

# Kategori kontrolü
try:
    pasta_category = ProductCategory.objects.get(name='PASTA ÇEŞİTLERİ')
    print(f"✅ PASTA ÇEŞİTLERİ kategorisi bulundu: {pasta_category}")
except ProductCategory.DoesNotExist:
    print("❌ PASTA ÇEŞİTLERİ kategorisi bulunamadı!")
    categories = ProductCategory.objects.all()
    print(f"Mevcut kategoriler: {[c.name for c in categories]}")

# Pasta ürünleri kontrolü
pasta_products = Product.objects.filter(category__name='PASTA ÇEŞİTLERİ', is_active=True)
print(f"\n✅ Aktif pasta ürünü sayısı: {pasta_products.count()}")

if pasta_products.exists():
    print("\nİlk 5 pasta ürünü:")
    for p in pasta_products[:5]:
        print(f"  - '{p.name}' (ID: {p.id})")
        
    # ' - ' içeren ürünler
    dash_products = pasta_products.filter(name__contains=' - ')
    print(f"\n✅ ' - ' içeren pasta ürünü sayısı: {dash_products.count()}")
    
    if dash_products.exists():
        print("İlk 3 ' - ' içeren ürün:")
        for p in dash_products[:3]:
            base_name, size = p.name.split(' - ', 1)
            print(f"  - '{p.name}' → base: '{base_name}', size: '{size}'")
    else:
        print("❌ ' - ' içeren pasta ürünü bulunamadı!")
else:
    print("❌ Hiç aktif pasta ürünü bulunamadı!")

print("\n=== DEBUG TAMAMLANDI ===")
