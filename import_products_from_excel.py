#!/usr/bin/env python
"""
Excel'deki ürün listesini Django sistemine aktar
"""
import os
import sys
import django
import pandas as pd
from pathlib import Path
from decimal import Decimal

# Django ayarlarını yükle
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bakery_management.settings')
django.setup()

from inventory.models import Product, ProductCategory
from users.models import Branch

def create_default_category():
    """Varsayılan pasta kategorisi oluştur"""
    category, created = ProductCategory.objects.get_or_create(
        name='Pastalar',
        defaults={
            'description': 'Excel listesinden aktarılan pastalar',
            'is_active': True
        }
    )
    if created:
        print(f"✅ Kategori oluşturuldu: {category.name}")
    else:
        print(f"📋 Mevcut kategori kullanılıyor: {category.name}")
    return category

def import_products_from_excel():
    """Excel dosyasından ürünleri aktar"""
    try:
        excel_file = "YENİ PASTA  LİSTE YAZILIM.xlsx"
        
        if not os.path.exists(excel_file):
            print(f"❌ Excel dosyası bulunamadı: {excel_file}")
            return False
        
        print(f"📊 Excel dosyası okunuyor: {excel_file}")
        df = pd.read_excel(excel_file)
        
        # Varsayılan kategoriyi oluştur
        default_category = create_default_category()
        
        # Sütun isimlerini kontrol et
        print(f"\n📋 Excel sütunları: {list(df.columns)}")
        
        # İlk sütunu ürün adı olarak kabul et
        product_name_column = df.columns[0]
        print(f"📝 Ürün adı sütunu: {product_name_column}")
        
        # Fiyat sütunu varsa bul
        price_column = None
        for col in df.columns:
            if any(keyword in str(col).lower() for keyword in ['fiyat', 'price', 'tutar', 'tl']):
                price_column = col
                break
        
        if price_column:
            print(f"💰 Fiyat sütunu: {price_column}")
        else:
            print("⚠️  Fiyat sütunu bulunamadı, varsayılan fiyat kullanılacak")
        
        # Ürünleri aktar
        imported_count = 0
        skipped_count = 0
        
        for index, row in df.iterrows():
            product_name = str(row[product_name_column]).strip()
            
            # Boş satırları atla
            if pd.isna(row[product_name_column]) or not product_name or product_name.lower() in ['nan', '']:
                continue
            
            # Fiyatı al
            if price_column and not pd.isna(row[price_column]):
                try:
                    price = Decimal(str(row[price_column]).replace(',', '.'))
                except:
                    price = Decimal('10.00')  # Varsayılan fiyat
            else:
                price = Decimal('10.00')  # Varsayılan fiyat
            
            # SKU oluştur
            sku = f"PASTA-{str(index + 1).zfill(3)}"
            
            # Ürün var mı kontrol et
            if Product.objects.filter(name=product_name).exists():
                print(f"⚠️  Zaten mevcut: {product_name}")
                skipped_count += 1
                continue
            
            # Ürünü oluştur
            try:
                product = Product.objects.create(
                    name=product_name,
                    category=default_category,
                    description=f"Excel listesinden aktarılan pasta: {product_name}",
                    unit='adet',
                    price_per_unit=price,
                    cost_per_unit=price * Decimal('0.6'),  # %60 maliyet varsayımı
                    sku=sku,
                    is_active=True,
                    is_produced=True,
                    shelf_life_days=3  # Pasta için 3 gün raf ömrü
                )
                
                print(f"✅ Ürün eklendi: {product.name} - {product.price_per_unit} TL")
                imported_count += 1
                
            except Exception as e:
                print(f"❌ Ürün eklenirken hata: {product_name} - {str(e)}")
                continue
        
        print(f"\n📊 İçe aktarma tamamlandı!")
        print(f"   ✅ Eklenen ürün: {imported_count}")
        print(f"   ⚠️  Atlanan ürün: {skipped_count}")
        print(f"   📋 Toplam işlenen: {imported_count + skipped_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Excel import hatası: {e}")
        return False

def create_sample_branch():
    """Örnek şube oluştur"""
    branch, created = Branch.objects.get_or_create(
        name='Ana Şube',
        defaults={
            'address': 'Merkez Mah. Pasta Sok. No:1',
            'phone': '0212 123 45 67',
            'is_active': True
        }
    )
    if created:
        print(f"✅ Şube oluşturuldu: {branch.name}")
    else:
        print(f"📋 Mevcut şube: {branch.name}")
    return branch

if __name__ == "__main__":
    print("Excel ürün listesi Django sistemine aktarılıyor...\n")
    
    # Örnek şube oluştur
    create_sample_branch()
    
    # Ürünleri aktar
    if import_products_from_excel():
        print("\n🎉 Ürün aktarımı başarıyla tamamlandı!")
        print("Artık şube müdürleri bu ürünlerden sipariş oluşturabilir.")
    else:
        print("\n❌ Ürün aktarımı başarısız oldu.")
