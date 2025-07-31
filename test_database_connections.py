#!/usr/bin/env python
"""
Veritabanı bağlantılarını test et ve en iyi seçeneği belirle
"""
import os
import sys
import django
from pathlib import Path
import time

# Django ayarlarını yükle
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bakery_management.settings')
django.setup()

from django.db import connections
from django.core.exceptions import ImproperlyConfigured

def test_database_connection(db_alias):
    """Belirli bir veritabanı bağlantısını test et"""
    try:
        start_time = time.time()
        db = connections[db_alias]
        
        # Bağlantıyı test et
        with db.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            
        connection_time = time.time() - start_time
        
        print(f"✅ {db_alias} veritabanı bağlantısı başarılı!")
        print(f"   Bağlantı süresi: {connection_time:.3f} saniye")
        print(f"   Veritabanı: {db.settings_dict['NAME']}")
        print(f"   Host: {db.settings_dict['HOST']}:{db.settings_dict['PORT']}")
        print(f"   Kullanıcı: {db.settings_dict['USER']}")
        
        # Basit tablo kontrolü
        try:
            with db.cursor() as cursor:
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
            print(f"   Tablolar: {len(tables)} tablo bulundu")
        except Exception as e:
            print(f"   Tablo listesi alınamadı: {e}")
        
        return True, connection_time
        
    except Exception as e:
        print(f"❌ {db_alias} veritabanı bağlantısı başarısız!")
        print(f"   Hata: {str(e)}")
        return False, None

def main():
    """Tüm veritabanı bağlantılarını test et"""
    print("🔍 Veritabanı bağlantıları test ediliyor...\n")
    
    # Test edilecek veritabanları
    databases = ['default', 'coolify', 'viapos_local', 'viapos']
    
    successful_connections = []
    failed_connections = []
    
    for db_alias in databases:
        print(f"📡 {db_alias} veritabanını test ediliyor...")
        success, connection_time = test_database_connection(db_alias)
        
        if success:
            successful_connections.append((db_alias, connection_time))
        else:
            failed_connections.append(db_alias)
        
        print("-" * 50)
    
    # Sonuçları özetle
    print("\n📊 TEST SONUÇLARI:")
    print(f"✅ Başarılı bağlantılar: {len(successful_connections)}")
    print(f"❌ Başarısız bağlantılar: {len(failed_connections)}")
    
    if successful_connections:
        print("\n🎯 Kullanılabilir veritabanları (hız sırasına göre):")
        # Hıza göre sırala
        successful_connections.sort(key=lambda x: x[1])
        for db_alias, conn_time in successful_connections:
            print(f"   {db_alias}: {conn_time:.3f}s")
    
    if failed_connections:
        print(f"\n⚠️  Başarısız bağlantılar: {', '.join(failed_connections)}")
    
    # Öneriler
    print("\n💡 ÖNERİLER:")
    if len(successful_connections) >= 2:
        primary, secondary = successful_connections[0], successful_connections[1]
        print(f"   Primary DB: {primary[0]} (en hızlı)")
        print(f"   Fallback DB: {secondary[0]} (yedek)")
    elif len(successful_connections) == 1:
        print(f"   Sadece {successful_connections[0][0]} kullanılabilir")
        print("   ⚠️  Yedek veritabanı yok!")
    else:
        print("   ❌ Hiçbir veritabanına bağlanılamıyor!")
        print("   🔧 Veritabanı ayarlarını kontrol edin")

if __name__ == "__main__":
    main()