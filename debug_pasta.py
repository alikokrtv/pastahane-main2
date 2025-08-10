#!/usr/bin/env python
import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bakery_management.settings')
django.setup()

from inventory.models import Product

print("PASTA ÇEŞİTLERİ ürünleri:")
pasta_products = Product.objects.filter(category__name='PASTA ÇEŞİTLERİ')[:10]
for p in pasta_products:
    print(f"  '{p.name}'")
print(f"\nToplam: {Product.objects.filter(category__name='PASTA ÇEŞİTLERİ').count()}")

# Ayrıca ' - ' içeren ürünleri kontrol et
print("\n' - ' içeren pasta ürünleri:")
dash_products = pasta_products.filter(name__contains=' - ')[:5]
for p in dash_products:
    print(f"  '{p.name}'")
