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

def create_branches():
    """Vega ve Çarşı şubelerini oluştur"""
    branches = []
    
    # Vega şubesi
    vega_branch, created = Branch.objects.get_or_create(
        name='Vega',
        defaults={
            'branch_type': 'sales',
            'address': 'Vega AVM, İstanbul',
            'phone': '0212 456 78 90',
            'email': 'vega@tatopastabaklava.com',
            'is_active': True
        }
    )
    if created:
        print(f"✅ Şube oluşturuldu: {vega_branch.name}")
    else:
        print(f"📋 Mevcut şube: {vega_branch.name}")
    branches.append(vega_branch)
    
    # Çarşı şubesi
    carsi_branch, created = Branch.objects.get_or_create(
        name='Çarşı',
        defaults={
            'branch_type': 'sales',
            'address': 'Kapalıçarşı, İstanbul',
            'phone': '0212 567 89 01',
            'email': 'carsi@tatopastabaklava.com',
            'is_active': True
        }
    )
    if created:
        print(f"✅ Şube oluşturuldu: {carsi_branch.name}")
    else:
        print(f"📋 Mevcut şube: {carsi_branch.name}")
    branches.append(carsi_branch)
    
    # Fabrika şubesi
    factory_branch, created = Branch.objects.get_or_create(
        name='Fabrika',
        defaults={
            'branch_type': 'production',
            'address': 'Fabrika Mah. Üretim Sok. No:1',
            'phone': '0212 678 90 12',
            'email': 'fabrika@tatopastabaklava.com',
            'is_active': True
        }
    )
    if created:
        print(f"✅ Şube oluşturuldu: {factory_branch.name}")
    else:
        print(f"📋 Mevcut şube: {factory_branch.name}")
    branches.append(factory_branch)
    
    return branches

def create_branch_managers():
    """Vega ve Çarşı şube müdürlerini oluştur"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    # Şubeleri al
    try:
        vega_branch = Branch.objects.get(name='Vega')
        carsi_branch = Branch.objects.get(name='Çarşı')
    except Branch.DoesNotExist:
        print("❌ Şubeler bulunamadı. Önce şubeleri oluşturun.")
        return False
    
    # Vega şube müdürü
    vega_user, created = User.objects.get_or_create(
        username='vega_mudur',
        defaults={
            'first_name': 'Vega',
            'last_name': 'Şube Müdürü',
            'email': 'vega@tatopastabaklava.com',
            'role': 'branch_manager',
            'branch': vega_branch,
            'is_active': True,
            'phone': '0532 111 22 33'
        }
    )
    if created:
        vega_user.set_password('vega123')
        vega_user.save()
        print(f"✅ Vega şube müdürü oluşturuldu: {vega_user.username}")
    else:
        print(f"📋 Mevcut kullanıcı: {vega_user.username}")
    
    # Çarşı şube müdürü
    carsi_user, created = User.objects.get_or_create(
        username='carsi_mudur',
        defaults={
            'first_name': 'Çarşı',
            'last_name': 'Şube Müdürü',
            'email': 'carsi@tatopastabaklava.com',
            'role': 'branch_manager',
            'branch': carsi_branch,
            'is_active': True,
            'phone': '0532 444 55 66'
        }
    )
    if created:
        carsi_user.set_password('carsi123')
        carsi_user.save()
        print(f"✅ Çarşı şube müdürü oluşturuldu: {carsi_user.username}")
    else:
        print(f"📋 Mevcut kullanıcı: {carsi_user.username}")
    
    print("\n🔐 Giriş Bilgileri:")
    print(f"   Vega: Kullanıcı adı: vega_mudur, Şifre: vega123")
    print(f"   Çarşı: Kullanıcı adı: carsi_mudur, Şifre: carsi123")
    
    return True

if __name__ == "__main__":
    print("Excel ürün listesi Django sistemine aktarılıyor...\n")
    
    # Şubeleri oluştur
    create_branches()
    
    # Ürünleri aktar
    if import_products_from_excel():
        print("\n🎉 Ürün aktarımı başarıyla tamamlandı!")
    else:
        print("\n❌ Ürün aktarımı başarısız oldu.")
    
    # Şube müdürlerini oluştur
    print("\n👥 Şube müdürleri oluşturuluyor...")
    if create_branch_managers():
        print("\n🎉 Sistem kurulumu tamamlandı!")
        print("Artık şube müdürleri sisteme giriş yapıp sipariş oluşturabilir.")
    else:
        print("\n❌ Kullanıcı oluşturma başarısız oldu.")
