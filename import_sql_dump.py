#!/usr/bin/env python
"""
Viapos SQL dump dosyasını yerel MySQL veritabanına import et
"""
import mysql.connector
from mysql.connector import Error
import re

def import_sql_dump():
    """SQL dump dosyasını viapos_local veritabanına import et"""
    try:
        # MySQL bağlantısını kur
        connection = mysql.connector.connect(
            host='localhost',
            database='viapos_local',
            user='root',
            password='255223',
            charset='utf8mb4',
            autocommit=True
        )
        
        cursor = connection.cursor()
        
        # SQL dosyasını oku
        sql_file = 'viapospr2_site_1753946368.sql'
        print(f"SQL dosyası okunuyor: {sql_file}")
        
        with open(sql_file, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # SQL komutlarını ayır (basit yaklaşım)
        # MySQL dump dosyalarında genellikle ';' ile ayrılır
        sql_commands = []
        current_command = ""
        
        for line in sql_content.split('\n'):
            # Yorumları ve boş satırları atla
            line = line.strip()
            if line.startswith('--') or line.startswith('/*') or not line:
                continue
                
            current_command += line + ' '
            
            # Komut bitişini kontrol et
            if line.endswith(';'):
                if current_command.strip():
                    sql_commands.append(current_command.strip())
                current_command = ""
        
        print(f"Toplam {len(sql_commands)} SQL komutu bulundu")
        
        # SQL komutlarını execute et
        success_count = 0
        error_count = 0
        
        for i, command in enumerate(sql_commands):
            try:
                # MySQL özel komutlarını atla
                if command.startswith('/*!') or command.startswith('LOCK TABLES') or command.startswith('UNLOCK TABLES'):
                    continue
                    
                cursor.execute(command)
                success_count += 1
                
                if (i + 1) % 100 == 0:
                    print(f"İşlenen komut sayısı: {i + 1}/{len(sql_commands)}")
                    
            except Error as e:
                error_count += 1
                if error_count <= 5:  # İlk 5 hatayı göster
                    print(f"⚠️  Komut hatası: {str(e)[:100]}...")
        
        print(f"\n✅ SQL import tamamlandı!")
        print(f"   Başarılı komut: {success_count}")
        print(f"   Hatalı komut: {error_count}")
        
        # Tabloları kontrol et
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"   Import edilen tablo sayısı: {len(tables)}")
        
        if tables:
            print("   Tablolar:")
            for table in tables[:10]:
                print(f"     - {table[0]}")
            if len(tables) > 10:
                print(f"     ... ve {len(tables) - 10} tablo daha")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Import hatası: {e}")
        return False
    except Exception as e:
        print(f"❌ Genel hata: {e}")
        return False

def test_viapos_data():
    """Import edilen Viapos verilerini test et"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='viapos_local',
            user='root',
            password='255223',
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # Ayarlar tablosunu kontrol et
        cursor.execute("SELECT COUNT(*) FROM ayarlar")
        ayarlar_count = cursor.fetchone()[0]
        print(f"✅ Ayarlar tablosunda {ayarlar_count} kayıt bulundu")
        
        # İlk birkaç ayarı göster
        cursor.execute("SELECT * FROM ayarlar LIMIT 3")
        ayarlar = cursor.fetchall()
        if ayarlar:
            print("   Örnek ayarlar:")
            for ayar in ayarlar:
                print(f"     ID: {ayar[0]}, Şube: {ayar[1]}")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Veri testi hatası: {e}")
        return False

if __name__ == "__main__":
    print("Viapos SQL dump import işlemi başlatılıyor...\n")
    
    if import_sql_dump():
        print("\nViapos verileri test ediliyor...")
        test_viapos_data()
    else:
        print("Import işlemi başarısız oldu.")
