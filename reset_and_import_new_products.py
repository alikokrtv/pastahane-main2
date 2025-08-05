#!/usr/bin/env python
"""
Eski ürünleri temizle ve Excel'deki yeni ürün listesini aktar
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

def clear_existing_products():
    """Mevcut ürünleri temizle"""
    print("🗑️ Mevcut ürünler temizleniyor...")
    
    # Tüm ürünleri sil
    deleted_products = Product.objects.all().delete()
    deleted_categories = ProductCategory.objects.all().delete()
    
    print(f"✅ {deleted_products[0]} ürün silindi")
    print(f"✅ {deleted_categories[0]} kategori silindi")

def create_new_categories():
    """Excel'deki yeni kategorileri oluştur"""
    print("\n📂 Yeni kategoriler oluşturuluyor...")
    
    # Excel'deki renkli kategoriler (BATON PASTALAR kaldırıldı)
    categories = [
        {'name': 'TURTA PASTALAR', 'description': '4K, 0, 1, 2 kategorileri - Kırmızı alan', 'color': 'red'},
        {'name': 'DİLİM PASTALAR', 'description': 'Dilim halinde satılan pastalar - Sarı alan', 'color': 'yellow'},
        {'name': 'SARMA GURUBU', 'description': 'Sarma tarzı tatlılar - Sarı alan', 'color': 'yellow'},
        {'name': 'SPESYEL ÜRÜNLER', 'description': 'Özel ürünler - Gri alan', 'color': 'gray'},
        {'name': 'SÜTSÜZ TATLILAR', 'description': 'Sütsüz tatlı çeşitleri - Sarı alan', 'color': 'yellow'},
        {'name': 'PASTA ÇEŞİTLERİ', 'description': 'Genel pasta çeşitleri - Kırmızı alan', 'color': 'red'},
        {'name': 'EKLER ÇEŞİTLERİ', 'description': 'Ekler ve benzeri ürünler - Yeşil alan', 'color': 'green'},
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

def import_excel_products():
    """Excel'deki tam ürün listesini aktar"""
    
    # Eski ürünleri temizle
    clear_existing_products()
    
    # Yeni kategorileri oluştur
    categories = create_new_categories()
    
    # Excel'deki ürünler - tam liste (BATON PASTALAR kaldırıldı)
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
    
    print(f"\n📦 Ürünler sisteme aktarılıyor...")
    created_count = 0
    
    # Kategori bazında fiyat haritası
    price_map = {
        'TURTA PASTALAR': 45.00,      # 4K kategorisi
        'DİLİM PASTALAR': 12.00,      # ADET  
        'SARMA GURUBU': 35.00,        # TEPSİ
        'SPESYEL ÜRÜNLER': 25.00,     # TEPSİ
        'SÜTSÜZ TATLILAR': 20.00,     # ADET
        'PASTA ÇEŞİTLERİ': 35.00,     # ADET
        'EKLER ÇEŞİTLERİ': 8.00,      # TEPSİ
    }
    
    # Kategori bazında birim haritası
    unit_map = {
        'TURTA PASTALAR': 'adet',
        'DİLİM PASTALAR': 'adet',
        'SARMA GURUBU': 'tepsi',
        'SPESYEL ÜRÜNLER': 'tepsi',
        'SÜTSÜZ TATLILAR': 'adet',
        'PASTA ÇEŞİTLERİ': 'adet',
        'EKLER ÇEŞİTLERİ': 'tepsi',
    }
    
    for category_name, products in excel_products.items():
        category = categories[category_name]
        print(f"\n📂 {category_name} ({len(products)} ürün)...")
        
        for product_name in products:
            # SKU oluştur
            sku = f"NEW-{str(created_count + 1).zfill(4)}"
            
            price = Decimal(str(price_map.get(category_name, 20.00)))
            unit = unit_map.get(category_name, 'adet')
            
            try:
                # Ürünü oluştur
                product = Product.objects.create(
                    name=product_name,
                    category=category,
                    description=f"Excel listesi: {product_name}",
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
    
    print(f"\n🎉 Yeni sistem hazır!")
    print(f"   📂 Kategori: {len(categories)}")
    print(f"   📦 Ürün: {created_count}")
    print(f"   💾 Toplam: {Product.objects.count()}")

if __name__ == '__main__':
    import_excel_products()