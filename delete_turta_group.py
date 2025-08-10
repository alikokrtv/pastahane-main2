#!/usr/bin/env python
import os
import django

# Django ayarlarını yükle
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bakery_management.settings')
django.setup()

from inventory.models import Product, ProductCategory

print("=== TURTA PASTALAR GRUBU SİLME İŞLEMİ ===")

# 1. TURTA PASTALAR kategorisindeki tüm ürünleri bul
turta_category = ProductCategory.objects.filter(name='TURTA PASTALAR').first()

if turta_category:
    print(f"\n📂 Kategori bulundu: {turta_category.name}")
    
    # Kategorideki aktif ürünleri listele
    turta_products = Product.objects.filter(category=turta_category, is_active=True)
    
    if turta_products.exists():
        print(f"\n🗑️ Silinecek ürünler ({turta_products.count()} adet):")
        for product in turta_products:
            print(f"  - {product.name} (SKU: {product.sku})")
        
        # Ürünleri pasif yap (is_active=False)
        updated_count = turta_products.update(is_active=False)
        print(f"\n✅ {updated_count} ürün başarıyla silindi (is_active=False)")
    else:
        print("\nℹ️ Bu kategoride aktif ürün bulunamadı")
    
    # Kategoriyi de pasif yap
    turta_category.is_active = False
    turta_category.save()
    print(f"✅ '{turta_category.name}' kategorisi pasif yapıldı")
    
else:
    print("\n❌ 'TURTA PASTALAR' kategorisi bulunamadı")

# 2. TURTA içeren diğer ürünleri kontrol et
print("\n=== DİĞER TURTA ÜRÜNLERİ KONTROLÜ ===")
other_turta_products = Product.objects.filter(
    name__icontains='TURTA', 
    is_active=True
).exclude(category__name='TURTA PASTALAR')

if other_turta_products.exists():
    print(f"\n🔍 Diğer kategorilerde bulunan TURTA ürünleri ({other_turta_products.count()} adet):")
    for product in other_turta_products:
        category_name = product.category.name if product.category else 'Kategori Yok'
        print(f"  - {product.name} (Kategori: {category_name})")
    
    # Bu ürünleri de sil
    other_updated_count = other_turta_products.update(is_active=False)
    print(f"\n✅ {other_updated_count} diğer TURTA ürünü silindi")
else:
    print("\nℹ️ Diğer kategorilerde TURTA ürünü bulunamadı")

print("\n=== KONTROL LİSTESİ ===")

# Aktif kategorileri listele
print("\n📂 Aktif kategoriler:")
active_categories = ProductCategory.objects.filter(is_active=True)
for cat in active_categories:
    product_count = Product.objects.filter(category=cat, is_active=True).count()
    print(f"  - {cat.name}: {product_count} ürün")

# TURTA içeren aktif ürün var mı kontrol et
remaining_turta = Product.objects.filter(name__icontains='TURTA', is_active=True)
if remaining_turta.exists():
    print(f"\n⚠️ Hala aktif TURTA ürünleri var ({remaining_turta.count()} adet):")
    for product in remaining_turta:
        category_name = product.category.name if product.category else 'Kategori Yok'
        print(f"  - {product.name} (Kategori: {category_name})")
else:
    print("\n✅ Tüm TURTA ürünleri başarıyla silindi")

print("\n=== TURTA GRUBU SİLME İŞLEMİ TAMAMLANDI ===")
