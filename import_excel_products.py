#!/usr/bin/env python
"""
Excel'deki tam ürün listesini sisteme aktar
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

def create_categories():
    """Excel'deki kategorileri oluştur"""
    categories = [
        {'name': 'TURTA PASTALAR', 'description': 'Turta formatındaki pastalar'},
        {'name': 'BATON PASTALAR', 'description': 'Baton şeklindeki pastalar'},
        {'name': 'DİLİM PASTALAR', 'description': 'Dilim halinde satılan pastalar'},
        {'name': 'SARMA GURUBU', 'description': 'Sarma tarzı tatlılar'},
        {'name': 'SPESYEL ÜRÜNLER', 'description': 'Özel ürünler'},
        {'name': 'SÜTSÜZ TATLILAR', 'description': 'Sütsüz tatlı çeşitleri'},
        {'name': 'PASTA ÇEŞİTLERİ', 'description': 'Genel pasta çeşitleri'},
        {'name': 'EKLER ÇEŞİTLERİ', 'description': 'Ekler ve benzeri ürünler'},
    ]
    
    created_categories = {}
    for cat_data in categories:
        category, created = ProductCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description'], 'is_active': True}
        )
        created_categories[cat_data['name']] = category
        if created:
            print(f"✅ Kategori oluşturuldu: {category.name}")
        else:
            print(f"📋 Mevcut kategori: {category.name}")
    
    return created_categories

def import_all_products():
    """Excel'deki tüm ürünleri aktar"""
    
    # Kategorileri oluştur
    categories = create_categories()
    
    # Excel'deki ürünler - kategori bazında
    excel_products = {
        'TURTA PASTALAR': [
            'FISTIKLI ÇİKOLATA SİYAH',
            'FISTIKLI ÇİKOLATA BEYAZ', 
            'SİYAH + BEYAZ MAGNUM',
            'KROKANKLI ÇİKOLATA',
            'KESTANELİ ÇİKOLATA',
            'GOLD ÇİKOLATALI',
            'GÖKKUŞAĞI ÇİKOLATALI',
            'CANAJ KAKO TOZLU',
            'FRAMBUAZLI ÇİKOLATALI',
            'KALP ÇİKOLATALI KIRMIZI',
            'KALP ÇİKOLATALI MAGNUM SİYAH',
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
            'UĞUR BÖCEĞİ'
        ],
        'BATON PASTALAR': [
            'FISTIK ÇİKO MAGNUM SİYAH',
            'FISTIK ÇİKO MAGNUM BEYAZ',
            'KROKANKLI KAMEL ÇİKOLATA',
            'CANAJ KAKO TOZLU',
            'FRAMBUAZLI ÇİKOLATALI',
            'PROFİTEROLLU ÇİKOLATALI',
            'MUZ ÇİKOLATALI',
            'ÇİLEK ÇİKOLATA',
            'KARIŞIK MEYVELİ',
            'MUZLU BATON SARMA'
        ],
        'DİLİM PASTALAR': [
            'FISTIK ÇİKO MAGNUM SİYAH',
            'FISTIK ÇİKO MAGNUM BEYAZ',
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
        'SARMA GURUBU': [
            'TRALİÇE KARAMELLİ',
            'TRALİÇE FRAMBUAZLI',
            'MEYVELİ BAHÇE',
            'KARDELEN',
            'MİNİ SARMA',
            'TARTOLET'
        ],
        'SPESYEL ÜRÜNLER': [
            'İZMİR BOMBASI',
            'ŞİROZBEK ÇEŞİTLERİ'
        ],
        'SÜTSÜZ TATLILAR': [
            'SUPANGLE',
            'PROFİTEROL',
            'MAGNOLYA ÇİLEKLİ',
            'MAGNOLYA OREO BİSKİVİ',
            'MAGNOLYA YABANMERSİNİ',
            'MAGNOLYA FISTIKLI',
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
            'LOTUS PASTA',
            'PANDA',
            'BÖĞÜRTLENLI BEYAZ'
        ],
        'EKLER ÇEŞİTLERİ': [
            'SADE',
            'ÇİKOLATALI',
            'FRAMBUAZLI',
            'LİMONLU',
            'PORTALLI',
            'YABANMERSİNİ',
            'ÇİLEKLİ',
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
    
    created_count = 0
    skipped_count = 0
    
    for category_name, products in excel_products.items():
        category = categories[category_name]
        print(f"\n📂 {category_name} kategorisi işleniyor...")
        
        for product_name in products:
            # Ürün var mı kontrol et
            if Product.objects.filter(name=product_name).exists():
                print(f"⚠️  Zaten mevcut: {product_name}")
                skipped_count += 1
                continue
            
            # SKU oluştur
            sku = f"EXL-{str(created_count + 1).zfill(4)}"
            
            # Varsayılan fiyat (kategori bazında)
            price_map = {
                'TURTA PASTALAR': 45.00,
                'BATON PASTALAR': 40.00,
                'DİLİM PASTALAR': 12.00,
                'SARMA GURUBU': 35.00,
                'SPESYEL ÜRÜNLER': 25.00,
                'SÜTSÜZ TATLILAR': 20.00,
                'PASTA ÇEŞİTLERİ': 35.00,
                'EKLER ÇEŞİTLERİ': 8.00,
            }
            
            price = Decimal(str(price_map.get(category_name, 20.00)))
            
            try:
                # Ürünü oluştur
                product = Product.objects.create(
                    name=product_name,
                    category=category,
                    description=f"Excel listesinden: {product_name}",
                    unit='adet',
                    price_per_unit=price,
                    cost_per_unit=price * Decimal('0.6'),  # %60 maliyet
                    sku=sku,
                    is_active=True,
                    is_produced=True,
                    shelf_life_days=3
                )
                
                print(f"✅ {product.name} - ₺{product.price_per_unit}")
                created_count += 1
                
            except Exception as e:
                print(f"❌ Hata: {product_name} - {str(e)}")
                continue
    
    print(f"\n📊 İçe aktarma tamamlandı!")
    print(f"   ✅ Eklenen ürün: {created_count}")
    print(f"   ⚠️  Atlanan ürün: {skipped_count}")
    print(f"   📦 Toplam ürün: {Product.objects.count()}")

if __name__ == '__main__':
    import_all_products()