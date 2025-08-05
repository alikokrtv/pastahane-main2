#!/usr/bin/env python
"""
Görseldeki gibi kategorize edilebilecek örnek ürünler oluştur
"""
import os
import sys
import django
from pathlib import Path
from decimal import Decimal

# Django ayarlarını yükle
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bakery_management.settings')
django.setup()

from inventory.models import Product, ProductCategory

def create_default_category():
    """Varsayılan pasta kategorisi oluştur"""
    category, created = ProductCategory.objects.get_or_create(
        name='Pastalar',
        defaults={
            'description': 'Tüm pasta çeşitleri',
            'is_active': True
        }
    )
    if created:
        print(f"✅ Kategori oluşturuldu: {category.name}")
    else:
        print(f"📋 Mevcut kategori kullanılıyor: {category.name}")
    return category

def create_sample_products():
    """Görseldeki kategorilere uygun örnek ürünler oluştur"""
    
    # Varsayılan kategoriyi oluştur
    default_category = create_default_category()
    
    # Örnek ürünler - görseldeki kategorilere göre isimlendirilmiş
    sample_products = [
        # KREMALI PASTALAR kategorisine girecek ürünler
        {'name': 'Fıstıklı Beyaz Kremalı Pasta', 'price': 45.00},
        {'name': 'Vişneli Krema Pasta', 'price': 40.00},
        {'name': 'Çilekli Kremalı Pasta', 'price': 42.00},
        {'name': 'Muzlu Kremalı Pasta', 'price': 38.00},
        {'name': 'Frambuazlı Krema Pasta', 'price': 44.00},
        
        # EKMEKIN PASTALAR kategorisine girecek ürünler  
        {'name': 'Fıstıklı Çikolatalı Pasta', 'price': 50.00},
        {'name': 'Kakaolu Brownie Pasta', 'price': 48.00},
        {'name': 'Tiramisu Çikolata', 'price': 55.00},
        {'name': 'Çilek Çikolata Pasta', 'price': 46.00},
        {'name': 'Muz Çikolata Pasta', 'price': 44.00},
        
        # DİLİM PASTALAR kategorisine girecek ürünler
        {'name': 'Dilim Vişneli Pasta', 'price': 12.00},
        {'name': 'Parça Çilekli Pasta', 'price': 11.00},
        {'name': 'Dilim Tiramisu', 'price': 15.00},
        {'name': 'Parça Frambuazlı Pasta', 'price': 13.00},
        
        # SARMA GURUBU kategorisine girecek ürünler
        {'name': 'Tatlıce Karamelli Sarma', 'price': 35.00},
        {'name': 'Muzlu Baton Sarma', 'price': 32.00},
        {'name': 'Sarma Frambuazlı Rulo', 'price': 36.00},
        {'name': 'Meyveli Baton Sarma', 'price': 34.00},
        
        # SPESYEL ÜRÜNLER kategorisine girecek ürünler
        {'name': 'Özel İzmir Bombası', 'price': 25.00},
        {'name': 'Spesyal Şirozbek Çeşitleri', 'price': 28.00},
        {'name': 'Premium Lotus Pasta', 'price': 60.00},
        {'name': 'Özel Magnolya Çilekli', 'price': 52.00},
        
        # SÜTSÜZ TATLILAR kategorisine girecek ürünler
        {'name': 'Şerbetli Tatlı Supangle', 'price': 18.00},
        {'name': 'Sütsüz Profiterol', 'price': 22.00},
        {'name': 'Desert Magnolya Oreolu', 'price': 20.00},
        {'name': 'Tatlı Magnolya Yabanmersini', 'price': 24.00},
        
        # Diğer ürünler
        {'name': 'Krokan Özel', 'price': 30.00},
        {'name': 'Yabanmersini Özel', 'price': 26.00},
        {'name': 'Kirpi Tatlısı', 'price': 16.00},
        {'name': 'Uğur Böceği Pasta', 'price': 19.00},
    ]
    
    created_count = 0
    skipped_count = 0
    
    for product_data in sample_products:
        # Ürün var mı kontrol et
        if Product.objects.filter(name=product_data['name']).exists():
            print(f"⚠️  Zaten mevcut: {product_data['name']}")
            skipped_count += 1
            continue
        
        # SKU oluştur
        sku = f"SAMPLE-{str(created_count + 1).zfill(3)}"
        
        try:
            # Ürünü oluştur
            product = Product.objects.create(
                name=product_data['name'],
                category=default_category,
                description=f"Örnek ürün: {product_data['name']}",
                unit='adet',
                price_per_unit=Decimal(str(product_data['price'])),
                cost_per_unit=Decimal(str(product_data['price'])) * Decimal('0.6'),  # %60 maliyet
                sku=sku,
                is_active=True,
                is_produced=True,
                shelf_life_days=3  # Pasta için 3 gün raf ömrü
            )
            
            print(f"✅ Ürün eklendi: {product.name} - ₺{product.price_per_unit}")
            created_count += 1
            
        except Exception as e:
            print(f"❌ Ürün eklenirken hata: {product_data['name']} - {str(e)}")
            continue
    
    print(f"\n📊 İşlem tamamlandı!")
    print(f"   ✅ Eklenen ürün: {created_count}")
    print(f"   ⚠️  Atlanan ürün: {skipped_count}")
    print(f"   📦 Toplam ürün: {Product.objects.count()}")

if __name__ == '__main__':
    create_sample_products()