#!/usr/bin/env python
"""
Excel tablosuna göre final ürün güncellemeleri
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

def update_products_final():
    """Excel tablosuna göre final güncellemeler"""
    
    print("🔄 Final ürün güncellemeleri başlıyor...")
    
    # 1. Eski ürünleri temizle
    clear_existing_products()
    
    # 2. Yeni kategorileri oluştur
    categories = create_final_categories()
    
    # 3. Final ürünleri ekle
    import_final_products(categories)

def clear_existing_products():
    """Mevcut ürünleri temizle"""
    print("🗑️ Mevcut ürünler temizleniyor...")
    
    deleted_products = Product.objects.all().delete()
    deleted_categories = ProductCategory.objects.all().delete()
    
    print(f"✅ {deleted_products[0]} ürün silindi")
    print(f"✅ {deleted_categories[0]} kategori silindi")

def create_final_categories():
    """Final kategorileri oluştur"""
    print("\n📂 Final kategoriler oluşturuluyor...")
    
    # Excel'deki güncellenmiş kategoriler
    categories = [
        {'name': 'TURTA PASTALAR', 'description': '4K, 0, 1, 2 kategorileri - Kırmızı alan'},
        {'name': 'DİLİM PASTALAR', 'description': 'Dilim halinde satılan pastalar - Sarı alan'},
        {'name': 'TEPSİLİ ÜRÜNLER', 'description': 'Tepsi/Sarma tarzı ürünler - Sarı alan'},  # SARMA GURUBU → TEPSİLİ ÜRÜNLER
        {'name': 'SPESYEL ÜRÜNLER', 'description': 'Özel ürünler - Gri alan'},
        {'name': 'SÜTLÜ TATLILAR', 'description': 'Sütlü tatlı çeşitleri - Sarı alan'},  # SÜTSÜZ → SÜTLÜ
        {'name': 'PASTA ÇEŞİTLERİ', 'description': 'Genel pasta çeşitleri - Kırmızı alan'},
        {'name': 'EKLER ÇEŞİTLERİ', 'description': 'Ekler ve benzeri ürünler - Yeşil alan'},
    ]
    
    created_categories = {}
    for cat_data in categories:
        category, created = ProductCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description'], 'is_active': True}
        )
        created_categories[cat_data['name']] = category
        print(f"✅ {category.name}")
    
    return created_categories

def import_final_products(categories):
    """Final ürün listesini aktar"""
    
    # Excel'deki FINAL ürün listesi
    excel_products = {
        'TURTA PASTALAR': [
            'FISTIKLI ÇİKOLATA SİYAH',
            'FISTIKLI ÇİKOLATA BEYAZ', 
            'SİYAH + BEYAZ',  # MAGNUM kaldırıldı
            'KROKANKLI ÇİKOLATA',
            'KESTANELİ ÇİKOLATA',
            'GOLD ÇİKOLATALI',
            'GÖKKUŞAĞI ÇİKOLATALI',  # Eklendi
            'CANAJ KAKO TOZLU',
            'FRAMBUAZLI ÇİKOLATALI',
            'KALP ÇİKOLATALI KIRMIZI',
            'KALP ÇİKOLATALI SİYAH',  # MAGNUM kaldırıldı
            'KALP YABAN MERSİN ÇİKOLATALI',
            'YABAN MERSİNİ MUZ ÇİKOLATA',
            'PROFİTEROLLU ÇİKOLATALI',
            'PROFİTEROLLU MUZLU',
            'VİŞNE ÇİKOLATALI',
            'MUZLU ÇİKOLATALI',
            'MUZLU VE ÇİLEKLİ',
            'ÇİLEK VE ÇİKOLATA',
            'KARIŞIK MEYVELİ',
            'REDVELET KIRMIZI',
            'REDVELET MOR / SİYAH',
            'KÖSTEBEK MODELLİ PASTA',
            'UĞUR BÖCEĞİ',
            'PANDA',  # Eklendi
            'LOTUS PASTA'  # Eklendi
        ],
        'DİLİM PASTALAR': [
            'FISTIK ÇİKO SİYAH',  # MAGNUM kaldırıldı
            'FISTIK ÇİKO BEYAZ',  # MAGNUM kaldırıldı
            'KROKANKLI ÇİKOLATA',
            'UĞUR BÖCEĞİ',
            'PROFİTEROLLU',
            'KARIŞIK MEYVELİ',
            'ÇİLEK ÇİKOLATA',
            'REDVELET',
            'MUZ SARMA DİLİM',
            'MUZ ÇİKOLATALI',
            'KALP KIRMIZI',
            'FRAMBUAZLI ÇİKOLATALI',
            'MALAGA SİYAH',
            'MALAGA BEYAZ'
        ],
        'TEPSİLİ ÜRÜNLER': [  # SARMA GURUBU → TEPSİLİ ÜRÜNLER
            'TRALİÇE KARAMELLİ',
            'TRALİÇE FRAMBUAZLI',
            'MEYVELİ BAHÇE',
            'KARDELEN',
            'MİNİ SARMA',
            'TARTOLET',
            'KARDELEN TEPSİ',  # Eklendi
            'MALAGA TEPSİ'  # Eklendi
        ],
        'SPESYEL ÜRÜNLER': [
            'İZMİR BOMBASI'  # Sadece bu kaldı, ŞİROZBEK silindi
        ],
        'SÜTLÜ TATLILAR': [  # SÜTSÜZ → SÜTLÜ
            'SUPANGLE',
            'PROFİTEROL',
            'ÇİLEKLİ',  # MAGNOLYA kaldırıldı
            'OREO BİSKİVİ',  # MAGNOLYA kaldırıldı
            'YABANMERSİNİ',  # MAGNOLYA kaldırıldı
            'FISTIKLI',  # MAGNOLYA kaldırıldı
            'MUZLU SARMA DİLİM'
        ],
        'PASTA ÇEŞİTLERİ': [
            'FISTIKLI BEYAZ',
            'FISTIKLI SİYAH',
            'CANAJ',
            'PROFİTEROLLU',
            'KROKAN',
            'MUZLU ÇİKOLATALI',
            'KİRPİ',
            'UĞUR BÖCEĞİ',
            'YABANMERSİNİ',
            'MUZLU VE ÇİLEKLİ',
            'KARIŞIK MEYVELİ',
            'ÇİLEKLİ',
            'FRAMBUAZLI',
            'RED WELWET',
            'GÖKKUŞAĞI',
            'BÖĞÜRTLENLI BEYAZ'
        ],
        'EKLER ÇEŞİTLERİ': [
            'SADE',
            'ÇİKOLATALI',
            'FRAMBUAZLI',
            'LİMONLU',
            'PORTALLI',
            'YABANMERSİNİ',
            'ÇİLEKLİ BEYAZ',  # ÇİLEKLİ → ÇİLEKLİ BEYAZ
            'HİNDİSTAN CEVİZLİ',
            'FINDIK',
            'LOTUSLU',
            'KAHVELİ',
            'FISTIKLI',
            'EKLER SADE',
            'EKLER ÇİKOLATALI',
            'EKLER REDVEL TOZ',
            'EKLER BEYAZ SOSLU SİYAH ÇİZGİLİ',
            'EKLER KARAMEL KALEM',
            'EKLER BEYAZ KAKAO TOZLU',
            'EKLER ÇİLEKLİ',
            'EKLER BEYAZ SOSLU ÇİZGİLİ',
            'EKLER FRAMBUAZLI KALEM',
            'EKLER KURBAĞA'
        ]
    }
    
    print(f"\n📦 Final ürünler sisteme aktarılıyor...")
    created_count = 0
    
    # Kategori bazında fiyat haritası
    price_map = {
        'TURTA PASTALAR': 45.00,
        'DİLİM PASTALAR': 12.00,
        'TEPSİLİ ÜRÜNLER': 35.00,  # SARMA GURUBU → TEPSİLİ ÜRÜNLER
        'SPESYEL ÜRÜNLER': 25.00,
        'SÜTLÜ TATLILAR': 20.00,  # SÜTSÜZ → SÜTLÜ
        'PASTA ÇEŞİTLERİ': 35.00,
        'EKLER ÇEŞİTLERİ': 8.00,
    }
    
    # Kategori bazında birim haritası
    unit_map = {
        'TURTA PASTALAR': 'adet',
        'DİLİM PASTALAR': 'adet',
        'TEPSİLİ ÜRÜNLER': 'tepsi',  # SARMA → TEPSİ
        'SPESYEL ÜRÜNLER': 'tepsi',
        'SÜTLÜ TATLILAR': 'adet',
        'PASTA ÇEŞİTLERİ': 'adet',
        'EKLER ÇEŞİTLERİ': 'tepsi',
    }
    
    for category_name, products in excel_products.items():
        category = categories[category_name]
        print(f"\n📂 {category_name} ({len(products)} ürün)...")
        
        for product_name in products:
            # SKU oluştur
            sku = f"FINAL-{str(created_count + 1).zfill(4)}"
            
            price = Decimal(str(price_map.get(category_name, 20.00)))
            unit = unit_map.get(category_name, 'adet')
            
            try:
                # Ürünü oluştur
                product = Product.objects.create(
                    name=product_name,
                    category=category,
                    description=f"Final Excel listesi: {product_name}",
                    unit=unit,
                    price_per_unit=price,
                    cost_per_unit=price * Decimal('0.6'),  # %60 maliyet
                    sku=sku,
                    is_active=True,
                    is_produced=True,
                    shelf_life_days=3
                )
                
                print(f"  ✅ {product.name} - ₺{product.price_per_unit} ({unit})")
                created_count += 1
                
            except Exception as e:
                print(f"  ❌ Hata: {product_name} - {str(e)}")
                continue
    
    print(f"\n🎉 Final sistem hazır!")
    print(f"   📂 Kategori: {len(categories)}")
    print(f"   📦 Ürün: {created_count}")

if __name__ == '__main__':
    update_products_final()