#!/usr/bin/env python
"""
Viapos veritabanı bağlantısını test etmek için basit script
"""
import os
import sys
import django
import argparse
from pathlib import Path

# Django ayarlarını yükle
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bakery_management.settings')
django.setup()

from django.db import connections
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

def apply_overrides(args):
    """Argümanlarla gelen host/port/user/password değerlerini DATABASES['viapos'] üzerine uygula."""
    dbs = connections.databases  # settings.DATABASES referansı
    if 'viapos' not in dbs:
        raise ImproperlyConfigured("'viapos' veritabanı konfigürasyonu bulunamadı.")
    cfg = dbs['viapos']
    if args.host:
        cfg['HOST'] = args.host
    if args.port:
        cfg['PORT'] = str(args.port)
    if args.user:
        cfg['USER'] = args.user
    if args.password:
        cfg['PASSWORD'] = args.password


def test_viapos_connection():
    """Viapos veritabanı bağlantısını test et"""
    try:
        # Viapos veritabanı bağlantısını al (settings.DATABASES['viapos'])
        viapos_db = connections['viapos']
        # Bağlanmadan önce hangi host/port kullanılacak göster
        settings_dict = viapos_db.settings_dict
        print(f"   Kullanılacak host: {settings_dict.get('HOST')} | port: {settings_dict.get('PORT')}")
        
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
    parser = argparse.ArgumentParser(description="Viapos MySQL bağlantı testi")
    parser.add_argument("--host", help="MySQL host")
    parser.add_argument("--port", type=int, help="MySQL port")
    parser.add_argument("--user", help="MySQL kullanıcı adı")
    parser.add_argument("--password", help="MySQL parola")
    args = parser.parse_args()

    # Argümanlarla override uygula
    apply_overrides(args)

    print("Viapos veritabanı bağlantısı test ediliyor...")
    test_viapos_connection()
