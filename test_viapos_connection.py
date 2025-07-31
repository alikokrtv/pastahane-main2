#!/usr/bin/env python
"""
Viapos veritabanı bağlantısını test etmek için basit script
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

from django.db import connections
from django.core.exceptions import ImproperlyConfigured

def test_viapos_connection():
    """Viapos veritabanı bağlantısını test et"""
    try:
        # Yerel Viapos veritabanı bağlantısını al
        viapos_db = connections['viapos_local']
        
        # Bağlantıyı test et
        with viapos_db.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            
        print("✅ Viapos veritabanı bağlantısı başarılı!")
        print(f"   Test sorgusu sonucu: {result}")
        
        # Veritabanı bilgilerini göster
        print(f"   Veritabanı: {viapos_db.settings_dict['NAME']}")
        print(f"   Host: {viapos_db.settings_dict['HOST']}")
        print(f"   Port: {viapos_db.settings_dict['PORT']}")
        
        # Tabloları listele
        with viapos_db.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
        print(f"   Toplam tablo sayısı: {len(tables)}")
        if tables:
            print("   İlk 10 tablo:")
            for i, table in enumerate(tables[:10]):
                print(f"     - {table[0]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Viapos veritabanı bağlantısı başarısız!")
        print(f"   Hata: {str(e)}")
        return False

if __name__ == "__main__":
    print("Viapos veritabanı bağlantısı test ediliyor...")
    test_viapos_connection()
