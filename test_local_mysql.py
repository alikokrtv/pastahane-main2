#!/usr/bin/env python
"""
Yerel MySQL bağlantısını test et ve Viapos veritabanını oluştur
"""
import mysql.connector
from mysql.connector import Error

def test_mysql_connection():
    """Farklı parola kombinasyonları ile MySQL bağlantısını test et"""
    passwords = ['255223']
    
    for password in passwords:
        try:
            print(f"MySQL bağlantısı deneniyor (parola: {'boş' if password == '' else password})...")
            
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password=password,
                charset='utf8mb4'
            )
            
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            
            print(f"✅ MySQL bağlantısı başarılı!")
            print(f"   MySQL versiyonu: {version[0]}")
            print(f"   Kullanılan parola: {'boş' if password == '' else password}")
            
            # Mevcut veritabanlarını listele
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            print(f"   Mevcut veritabanları: {[db[0] for db in databases]}")
            
            cursor.close()
            connection.close()
            return password
            
        except Error as e:
            print(f"❌ Bağlantı başarısız: {e}")
            continue
    
    print("❌ Hiçbir parola kombinasyonu çalışmadı!")
    return None

def create_viapos_database(password):
    """Viapos veritabanını oluştur"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=password,
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # Veritabanını oluştur
        cursor.execute("DROP DATABASE IF EXISTS viapos_local")
        cursor.execute("CREATE DATABASE viapos_local CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print("✅ viapos_local veritabanı oluşturuldu")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Veritabanı oluşturma hatası: {e}")
        return False

if __name__ == "__main__":
    print("Yerel MySQL bağlantısı test ediliyor...\n")
    
    password = test_mysql_connection()
    if password is not None:
        print(f"\nViapos veritabanı oluşturuluyor...")
        create_viapos_database(password)
    else:
        print("\nMySQL bağlantısı kurulamadı. Lütfen MySQL ayarlarınızı kontrol edin.")
