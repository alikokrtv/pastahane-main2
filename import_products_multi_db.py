#!/usr/bin/env python
"""
Excel'deki ürün listesini birden fazla veritabanına aktar
"""
import os
import sys
import django
import pandas as pd
from pathlib import Path
from decimal import Decimal

# PyMySQL configuration for MySQL support
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

# Django ayarlarını yükle
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bakery_management.settings')
django.setup()

from django.db import connections, transaction
from inventory.models import Product, ProductCategory
from users.models import Branch

def test_database_connection(db_alias):
    """Veritabanı bağlantısını test et"""
    try:
        db = connections[db_alias]
        with db.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        return True
    except Exception as e:
        print(f"❌ {db_alias} veritabanı bağlantısı başarısız: {e}")
        return False

def get_available_databases():
    """Kullanılabilir veritabanlarını listele"""
    available_dbs = []
    test_databases = ['default', 'viapos_local', 'coolify', 'viapos']
    
    for db_alias in test_databases:
        try:
            if test_database_connection(db_alias):
                available_dbs.append(db_alias)
                print(f"✅ {db_alias} veritabanı kullanılabilir")
        except Exception:
            continue
    
    return available_dbs

def create_default_category(using_db='default'):
    """Varsayılan pasta kategorisi oluştur"""
    try:
        category, created = ProductCategory.objects.using(using_db).get_or_create(
            name='Pastalar',
            defaults={
                'description': 'Excel listesinden aktarılan pastalar',
                'is_active': True
            }
        )
        if created:
            print(f"✅ [{using_db}] Kategori oluşturuldu: {category.name}")
        else:
            print(f"📋 [{using_db}] Mevcut kategori kullanılıyor: {category.name}")
        return category
    except Exception as e:
        print(f"❌ [{using_db}] Kategori oluşturulamadı: {e}")
        return None

def create_sample_branch(using_db='default'):
    """Örnek şube oluştur"""
    try:
        branch, created = Branch.objects.using(using_db).get_or_create(
            name='Ana Şube',
            defaults={
                'address': 'Merkez Mah. Pasta Sok. No:1',
                'phone': '0212 123 45 67',
                'is_active': True
            }
        )
        if created:
            print(f"✅ [{using_db}] Şube oluşturuldu: {branch.name}")
        else:
            print(f"📋 [{using_db}] Mevcut şube: {branch.name}")
        return branch
    except Exception as e:
        print(f"❌ [{using_db}] Şube oluşturulamadı: {e}")
        return None

def import_products_to_database(db_alias, excel_file):
    """Belirli bir veritabanına ürünleri aktar"""
    print(f"\n🔄 [{db_alias}] veritabanına ürün aktarımı başlıyor...")
    
    try:
        # Excel dosyasını oku
        if not os.path.exists(excel_file):
            print(f"❌ Excel dosyası bulunamadı: {excel_file}")
            return False
        
        df = pd.read_excel(excel_file)
        print(f"📊 [{db_alias}] Excel dosyası okundu: {len(df)} satır")
        
        # Sütun isimlerini kontrol et
        print(f"📋 [{db_alias}] Excel sütunları: {list(df.columns)}")
        
        # İlk sütunu ürün adı olarak kabul et
        if len(df.columns) == 0:
            print(f"❌ [{db_alias}] Excel dosyası boş!")
            return False
        
        product_name_column = df.columns[0]
        print(f"📝 [{db_alias}] Ürün adı sütunu: {product_name_column}")
        
        # Fiyat sütunu varsa bul
        price_column = None
        for col in df.columns:
            if any(keyword in str(col).lower() for keyword in ['fiyat', 'price', 'tutar', 'tl']):
                price_column = col
                break
        
        if price_column:
            print(f"💰 [{db_alias}] Fiyat sütunu: {price_column}")
        else:
            print(f"⚠️  [{db_alias}] Fiyat sütunu bulunamadı, varsayılan fiyat kullanılacak")
        
        # Kategori ve şube oluştur
        default_category = create_default_category(using_db=db_alias)
        if not default_category:
            return False
        
        sample_branch = create_sample_branch(using_db=db_alias)
        if not sample_branch:
            return False
        
        # Ürünleri aktar
        imported_count = 0
        skipped_count = 0
        error_count = 0
        
        with transaction.atomic(using=db_alias):
            for index, row in df.iterrows():
                try:
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
                    if Product.objects.using(db_alias).filter(name=product_name).exists():
                        print(f"⚠️  [{db_alias}] Zaten mevcut: {product_name}")
                        skipped_count += 1
                        continue
                    
                    # Ürünü oluştur
                    product = Product.objects.using(db_alias).create(
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
                    
                    print(f"✅ [{db_alias}] Ürün eklendi: {product.name} - {product.price_per_unit} TL")
                    imported_count += 1
                    
                except Exception as e:
                    print(f"❌ [{db_alias}] Ürün eklenirken hata: {product_name} - {str(e)}")
                    error_count += 1
                    continue
        
        print(f"\n📊 [{db_alias}] İçe aktarma tamamlandı!")
        print(f"   ✅ Eklenen ürün: {imported_count}")
        print(f"   ⚠️  Atlanan ürün: {skipped_count}")
        print(f"   ❌ Hatalı ürün: {error_count}")
        print(f"   📋 Toplam işlenen: {imported_count + skipped_count + error_count}")
        
        return imported_count > 0
        
    except Exception as e:
        print(f"❌ [{db_alias}] Excel import hatası: {e}")
        return False

def main():
    """Ana import fonksiyonu"""
    excel_file = "YENİ PASTA  LİSTE YAZILIM.xlsx"
    
    print("🚀 Çoklu veritabanı ürün aktarımı başlıyor...")
    print(f"📁 Excel dosyası: {excel_file}")
    
    # Kullanılabilir veritabanlarını test et
    print("\n🔍 Veritabanları kontrol ediliyor...")
    available_dbs = get_available_databases()
    
    if not available_dbs:
        print("❌ Hiçbir veritabanı kullanılabilir değil!")
        return False
    
    print(f"\n📈 {len(available_dbs)} veritabanı kullanılabilir: {', '.join(available_dbs)}")
    
    # Her kullanılabilir veritabanına aktar
    successful_imports = []
    failed_imports = []
    
    for db_alias in available_dbs:
        print(f"\n{'='*60}")
        success = import_products_to_database(db_alias, excel_file)
        
        if success:
            successful_imports.append(db_alias)
        else:
            failed_imports.append(db_alias)
    
    # Sonuç özeti
    print(f"\n{'='*60}")
    print("🎯 AKTARIM ÖZETI:")
    print(f"✅ Başarılı aktarımlar: {len(successful_imports)}")
    if successful_imports:
        for db in successful_imports:
            print(f"   - {db}")
    
    print(f"❌ Başarısız aktarımlar: {len(failed_imports)}")
    if failed_imports:
        for db in failed_imports:
            print(f"   - {db}")
    
    if successful_imports:
        print("\n🎉 Ürün aktarımı tamamlandı!")
        print("Şube müdürleri artık bu ürünlerden sipariş oluşturabilir.")
        return True
    else:
        print("\n❌ Hiçbir veritabanına ürün aktarılamadı!")
        return False

if __name__ == "__main__":
    main()