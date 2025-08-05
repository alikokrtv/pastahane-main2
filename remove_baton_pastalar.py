#!/usr/bin/env python
"""
BATON PASTALAR kategorisini ve ürünlerini sil
"""
import os
import sys
import django
from pathlib import Path

# Django ayarlarını yükle
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bakery_management.settings')
django.setup()

from inventory.models import Product, ProductCategory

def remove_baton_pastalar():
    """BATON PASTALAR kategorisini ve ürünlerini sil"""
    
    print("🗑️ BATON PASTALAR kategorisi siliniyor...")
    
    try:
        # BATON PASTALAR kategorisini bul
        baton_category = ProductCategory.objects.get(name='BATON PASTALAR')
        
        # Bu kategorideki ürünleri listele
        baton_products = Product.objects.filter(category=baton_category)
        product_count = baton_products.count()
        
        print(f"📋 BATON PASTALAR kategorisinde {product_count} ürün bulundu:")
        for product in baton_products:
            print(f"  • {product.name}")
        
        if product_count > 0:
            # Ürünleri sil
            deleted_products = baton_products.delete()
            print(f"✅ {deleted_products[0]} ürün silindi")
        
        # Kategoriyi sil
        baton_category.delete()
        print(f"✅ BATON PASTALAR kategorisi silindi")
        
        # Template'deki kategorileme fonksiyonunu güncelle
        print("\n🔧 Kategorileme sistemi güncelleniyor...")
        update_categorization_system()
        
        print(f"\n🎉 İşlem tamamlandı!")
        print(f"   📂 Kalan kategori sayısı: {ProductCategory.objects.count()}")
        print(f"   📦 Kalan ürün sayısı: {Product.objects.count()}")
        
    except ProductCategory.DoesNotExist:
        print("⚠️ BATON PASTALAR kategorisi bulunamadı (zaten silinmiş olabilir)")
        
    except Exception as e:
        print(f"❌ Hata oluştu: {str(e)}")

def update_categorization_system():
    """Kategorileme sisteminde BATON PASTALAR referanslarını temizle"""
    
    # Yeni kategoriler listesi (BATON PASTALAR olmadan)
    remaining_categories = [
        'TURTA PASTALAR',
        'DİLİM PASTALAR', 
        'SARMA GURUBU',
        'SPESYEL ÜRÜNLER',
        'SÜTSÜZ TATLILAR',
        'PASTA ÇEŞİTLERİ',
        'EKLER ÇEŞİTLERİ'
    ]
    
    print("📝 Güncellenen kategoriler:")
    for i, cat in enumerate(remaining_categories, 1):
        print(f"   {i}. {cat}")

if __name__ == '__main__':
    remove_baton_pastalar()