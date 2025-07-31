#!/usr/bin/env python
"""
Yerel Viapos veritabanının durumunu kontrol et
"""
import mysql.connector
from mysql.connector import Error

def check_viapos_database():
    """Viapos yerel veritabanının durumunu kontrol et"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='viapos_local',
            user='root',
            password='255223',
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # Tabloları listele
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print(f"✅ Viapos yerel veritabanına bağlantı başarılı!")
        print(f"   Toplam tablo sayısı: {len(tables)}")
        
        if tables:
            print("\n📋 Mevcut tablolar:")
            for i, table in enumerate(tables, 1):
                table_name = table[0]
                
                # Her tablo için kayıt sayısını al
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
                    count = cursor.fetchone()[0]
                    print(f"   {i:2d}. {table_name} ({count} kayıt)")
                except Error as e:
                    print(f"   {i:2d}. {table_name} (kayıt sayısı alınamadı: {str(e)[:50]}...)")
        else:
            print("   Hiç tablo bulunamadı.")
        
        cursor.close()
        connection.close()
        return len(tables) > 0
        
    except Error as e:
        print(f"❌ Veritabanı bağlantı hatası: {e}")
        return False

def update_django_settings():
    """Django settings.py dosyasını yerel Viapos veritabanı için güncelle"""
    print("\n🔧 Django ayarları güncelleniyor...")
    
    settings_content = '''
    # Yerel Viapos veritabanı bağlantısı
    'viapos_local': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'viapos_local',
        'USER': 'root',
        'PASSWORD': '255223',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'connect_timeout': 20,
        },
    }'''
    
    print("Django settings.py dosyasına aşağıdaki bağlantı bilgilerini ekleyebilirsiniz:")
    print(settings_content)
    return True

if __name__ == "__main__":
    print("Viapos yerel veritabanı durumu kontrol ediliyor...\n")
    
    if check_viapos_database():
        update_django_settings()
        print("\n✅ Viapos yerel veritabanı hazır!")
        print("   Artık Django uygulamanızda bu veritabanını kullanabilirsiniz.")
    else:
        print("\n❌ Viapos veritabanında sorun var. Import işlemini tekrar deneyebiliriz.")
