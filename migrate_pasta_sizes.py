#!/usr/bin/env python
"""
Production Migration Script: Pasta Çeşitleri Boyutlu Ürünler
Bu script mevcut pasta ürünlerini alıp her biri için 4K, 0, 1, 2 boyutlarında yeni ürünler oluşturur.
"""
import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bakery_management.settings')
django.setup()

from inventory.models import Product, ProductCategory

def migrate_pasta_sizes():
    """Mevcut pasta ürünlerini boyutlu versiyonlara çevir"""
    
    print("=== PASTA ÇEŞİTLERİ BOYUT MİGRASYONU ===")
    
    # PASTA ÇEŞİTLERİ kategorisini al
    try:
        pasta_category = ProductCategory.objects.get(name='PASTA ÇEŞİTLERİ')
        print(f"✅ Kategori bulundu: {pasta_category}")
    except ProductCategory.DoesNotExist:
        print("❌ PASTA ÇEŞİTLERİ kategorisi bulunamadı!")
        return
    
    # Mevcut boyutsuz pasta ürünlerini al
    existing_products = Product.objects.filter(
        category=pasta_category,
        is_active=True
    ).exclude(name__contains=' - ')  # Boyut bilgisi olmayanları al
    
    print(f"✅ Boyutsuz pasta ürünü sayısı: {existing_products.count()}")
    
    if not existing_products.exists():
        print("❌ Boyutsuz pasta ürünü bulunamadı!")
        return
    
    # Boyut tanımları
    sizes = [
        {'code': 'K4', 'display': '4K'},
        {'code': 'No0', 'display': '0'},
        {'code': 'No1', 'display': '1'},
        {'code': 'No2', 'display': '2'}
    ]
    
    created_count = 0
    
    for product in existing_products:
        print(f"\n🔄 İşleniyor: {product.name}")
        
        # Bu ürün için boyutlu versiyonlar oluştur
        for size in sizes:
            new_name = f"{product.name} - {size['code']}"
            
            # Aynı isimde ürün var mı kontrol et
            if Product.objects.filter(name=new_name).exists():
                print(f"  ⚠️  Zaten mevcut: {new_name}")
                continue
            
            # Yeni boyutlu ürün oluştur
            new_product = Product.objects.create(
                name=new_name,
                category=product.category,
                price=product.price,
                cost=product.cost,
                sku=f"{product.sku}-{size['code']}" if product.sku else None,
                description=f"{product.description} - {size['display']} Boyut" if product.description else f"{size['display']} Boyut",
                is_active=True,
                quantity=product.quantity,
                minimum_stock=product.minimum_stock
            )
            
            print(f"  ✅ Oluşturuldu: {new_product.name}")
            created_count += 1
        
        # Orijinal boyutsuz ürünü pasif yap (silme, sadece gizle)
        product.is_active = False
        product.save()
        print(f"  🔒 Orijinal ürün pasif yapıldı: {product.name}")
    
    print(f"\n🎉 MİGRASYON TAMAMLANDI!")
    print(f"✅ {created_count} yeni boyutlu ürün oluşturuldu")
    print(f"🔒 {existing_products.count()} orijinal ürün pasif yapıldı")
    
    # Sonuçları kontrol et
    print("\n=== SONUÇ KONTROLÜ ===")
    new_products = Product.objects.filter(
        category=pasta_category,
        is_active=True,
        name__contains=' - '
    )
    print(f"✅ Aktif boyutlu pasta ürünü sayısı: {new_products.count()}")
    
    # Örnek ürünler göster
    print("\nÖrnek boyutlu ürünler:")
    for product in new_products[:8]:
        print(f"  - {product.name}")

if __name__ == "__main__":
    # Güvenlik onayı
    response = input("Bu script production database'i değiştirecek. Devam etmek istiyor musunuz? (yes/no): ")
    if response.lower() in ['yes', 'y', 'evet', 'e']:
        migrate_pasta_sizes()
    else:
        print("❌ İşlem iptal edildi.")
