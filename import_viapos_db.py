#!/usr/bin/env python
"""
Viapos SQL dump dosyasını yerel MySQL sunucusuna import etmek için script
"""
import os
import sys
import subprocess
import mysql.connector
from mysql.connector import Error

def create_viapos_database():
    """Yerel MySQL sunucusunda Viapos veritabanını oluştur"""
    try:
        # MySQL root kullanıcısı ile bağlan
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # Yerel MySQL root parolası (genellikle boş)
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # Veritabanını oluştur
        cursor.execute("CREATE DATABASE IF NOT EXISTS viapos_local CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print("✅ Viapos yerel veritabanı oluşturuldu/kontrol edildi")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ MySQL bağlantı hatası: {e}")
        return False

def import_sql_dump():
    """SQL dump dosyasını yerel veritabanına import et"""
    try:
        sql_file = "viapospr2_site_1753946368.sql"
        
        # MySQL komut satırı ile import et
        cmd = [
            "mysql",
            "-u", "root",
            "-p",  # Parola istenecek
            "viapos_local"
        ]
        
        print("MySQL import işlemi başlatılıyor...")
        print("MySQL root parolasını girmeniz istenecek.")
        
        with open(sql_file, 'r', encoding='utf-8') as file:
            process = subprocess.run(
                cmd,
                stdin=file,
                capture_output=True,
                text=True
            )
        
        if process.returncode == 0:
            print("✅ SQL dump dosyası başarıyla import edildi!")
            return True
        else:
            print(f"❌ Import hatası: {process.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Import işlemi hatası: {e}")
        return False

def test_local_viapos_connection():
    """Yerel Viapos veritabanı bağlantısını test et"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='viapos_local',
            user='root',
            password='',  # Yerel MySQL root parolası
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # Tabloları listele
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print(f"✅ Yerel Viapos veritabanı bağlantısı başarılı!")
        print(f"   Toplam tablo sayısı: {len(tables)}")
        
        if tables:
            print("   Tablolar:")
            for table in tables[:10]:  # İlk 10 tabloyu göster
                print(f"     - {table[0]}")
            if len(tables) > 10:
                print(f"     ... ve {len(tables) - 10} tablo daha")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Yerel veritabanı bağlantı hatası: {e}")
        return False

if __name__ == "__main__":
    print("Viapos yerel veritabanı kurulumu başlatılıyor...\n")
    
    # 1. Veritabanını oluştur
    if create_viapos_database():
        print()
        
        # 2. SQL dump'ı import et
        if import_sql_dump():
            print()
            
            # 3. Bağlantıyı test et
            test_local_viapos_connection()
        else:
            print("SQL import işlemi başarısız oldu.")
    else:
        print("Veritabanı oluşturma işlemi başarısız oldu.")
