#!/usr/bin/env python3
"""
Tam kurulum paketi oluşturucu - Hem temel hem gelişmiş sürüm
"""

import os
import shutil
from pathlib import Path

def create_complete_package():
    """Tam kurulum paketi oluştur"""
    
    print("📦 Tato Pasta & Baklava - TAM KURULUM PAKETİ")
    print("=" * 60)
    
    # EXE dosyalarını kontrol et
    basic_exe = "dist/FabrikaYaziciSistemi.exe"
    advanced_exe = "dist/GelismisFabrikaYazici.exe"
    
    basic_exists = os.path.exists(basic_exe)
    advanced_exists = os.path.exists(advanced_exe)
    
    print(f"📋 Mevcut EXE dosyaları:")
    print(f"   Temel Sürüm: {'✅' if basic_exists else '❌'} {basic_exe}")
    print(f"   Gelişmiş Sürüm: {'✅' if advanced_exists else '❌'} {advanced_exe}")
    
    if not (basic_exists or advanced_exists):
        print("❌ Hiçbir EXE dosyası bulunamadı!")
        return False
    
    # Ana kurulum klasörü oluştur
    package_dir = "FabrikaYaziciSistemi_TAM_PAKET"
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
        print(f"🗑️ Eski paket temizlendi: {package_dir}")
    
    os.makedirs(package_dir)
    print(f"📁 Ana paket klasörü oluşturuldu: {package_dir}")
    
    # Alt klasörler oluştur
    basic_dir = os.path.join(package_dir, "1_Temel_Surum")
    advanced_dir = os.path.join(package_dir, "2_Gelismis_Surum")
    docs_dir = os.path.join(package_dir, "3_Dokumantasyon")
    
    if basic_exists:
        os.makedirs(basic_dir)
        print(f"📁 Temel sürüm klasörü oluşturuldu")
    
    if advanced_exists:
        os.makedirs(advanced_dir)
        print(f"📁 Gelişmiş sürüm klasörü oluşturuldu")
    
    os.makedirs(docs_dir)
    print(f"📁 Dokümantasyon klasörü oluşturuldu")
    
    # 1. Temel sürümü kopyala
    if basic_exists:
        copy_basic_version(basic_dir, basic_exe)
    
    # 2. Gelişmiş sürümü kopyala
    if advanced_exists:
        copy_advanced_version(advanced_dir, advanced_exe)
    
    # 3. Dokümantasyon kopyala
    copy_documentation(docs_dir)
    
    # 4. Ana başlatma dosyaları oluştur
    create_main_launchers(package_dir, basic_exists, advanced_exists)
    
    # 5. Ana README oluştur
    create_main_readme(package_dir, basic_exists, advanced_exists)
    
    # Paket içeriğini göster
    show_complete_package_contents(package_dir)
    
    print(f"\n🎉 TAM KURULUM PAKETİ HAZIR!")
    print(f"📂 Konum: {os.path.abspath(package_dir)}")
    
    return True

def copy_basic_version(basic_dir, basic_exe):
    """Temel sürümü kopyala"""
    print("\n📋 Temel sürüm hazırlanıyor...")
    
    # EXE dosyasını kopyala
    shutil.copy2(basic_exe, basic_dir)
    
    # Başlatma scripti
    basic_launcher = """@echo off
title Temel Fabrika Yazici Sistemi
cls
color 0A

echo.
echo  ===============================================
echo         TEMEL FABRİKA YAZICI SİSTEMİ
echo  ===============================================
echo.
echo  📋 Kolay kullanım için tasarlandı
echo  🖨️  Otomatik yazdırma
echo  📊 Temel durum takibi
echo.
echo  Program başlatılıyor...
echo.

cd /d "%~dp0"

if exist "FabrikaYaziciSistemi.exe" (
    start "" "FabrikaYaziciSistemi.exe"
    echo  ✅ Temel sürüm başlatıldı!
    timeout /t 3 >nul
) else (
    echo  ❌ EXE dosyası bulunamadı!
    pause
)
"""
    
    with open(os.path.join(basic_dir, "Temel_Baslatma.bat"), 'w', encoding='utf-8') as f:
        f.write(basic_launcher)
    
    # Temel sürüm README
    basic_readme = """
🏭 TEMEL FABRİKA YAZICI SİSTEMİ
==============================

✨ ÖZELLIKLER
- Basit ve kullanıcı dostu arayüz
- Otomatik sipariş dinleme
- Hızlı yazdırma
- Temel durum gösterimi

🚀 KULLANIM
1. "Temel_Baslatma.bat" dosyasına çift tıklayın
2. "Bağlantı Testi" yapın
3. "Başlat" butonuna tıklayın
4. Sistem otomatik çalışmaya başlar

👥 KİMLER İÇİN
- Basit kullanım isteyen fabrikalar
- Az özellikle yetinen kullanıcılar
- Hızlı kurulum isteyenler
"""
    
    with open(os.path.join(basic_dir, "TEMEL_SURUM_REHBERI.txt"), 'w', encoding='utf-8') as f:
        f.write(basic_readme)
    
    print("✅ Temel sürüm hazırlandı")

def copy_advanced_version(advanced_dir, advanced_exe):
    """Gelişmiş sürümü kopyala"""
    print("\n📋 Gelişmiş sürüm hazırlanıyor...")
    
    # EXE dosyasını kopyala
    shutil.copy2(advanced_exe, advanced_dir)
    
    # Gelişmiş başlatma scripti
    advanced_launcher = """@echo off
title Gelismis Fabrika Yazici Sistemi
cls
color 0B

echo.
echo  ===============================================
echo        GELİŞMİŞ FABRİKA YAZICI SİSTEMİ
echo  ===============================================
echo.
echo  🖨️  Otomatik yazıcı algılama
echo  📊 Detaylı durum takibi
echo  🔧 Gelişmiş ayarlar
echo  📝 Kapsamlı log sistemi
echo.
echo  Program başlatılıyor...
echo.

cd /d "%~dp0"

if exist "GelismisFabrikaYazici.exe" (
    start "" "GelismisFabrikaYazici.exe"
    echo  ✅ Gelişmiş sürüm başlatıldı!
    timeout /t 3 >nul
) else (
    echo  ❌ EXE dosyası bulunamadı!
    pause
)
"""
    
    with open(os.path.join(advanced_dir, "Gelismis_Baslatma.bat"), 'w', encoding='utf-8') as f:
        f.write(advanced_launcher)
    
    # Gelişmiş sürüm README
    advanced_readme = """
🏭 GELİŞMİŞ FABRİKA YAZICI SİSTEMİ
==================================

⭐ ÖZELLIKLER
- Otomatik yazıcı algılama ve durum kontrolü
- Sekmeli arayüz (Ana Kontrol/Yazıcı/Ayarlar/Loglar)
- Test yazdırma özellikleri
- Detaylı log sistemi
- Yazıcı yönetimi
- Gelişmiş ayarlar

🖨️ YAZICI YÖNETİMİ
- Sistemdeki tüm yazıcıları otomatik bulur
- Yazıcı durumlarını kontrol eder (Hazır/Çevrimdışı/Hata/etc.)
- Test yazdırma özelliği
- Yazıcı seçimi ve ayarları

🚀 KULLANIM
1. "Gelismis_Baslatma.bat" dosyasına çift tıklayın
2. "Yazıcı Yönetimi" sekmesinden yazıcıyı seçin
3. "Ana Kontrol" sekmesinde "Bağlantı Testi" yapın
4. "Başlat" butonuna tıklayın

🎯 KİMLER İÇİN
- Detaylı kontrol isteyen fabrikalar
- Birden fazla yazıcısı olan işletmeler
- Gelişmiş özellik isteyenler
- Teknik bilgi sahibi kullanıcılar
"""
    
    with open(os.path.join(advanced_dir, "GELISMIS_SURUM_REHBERI.txt"), 'w', encoding='utf-8') as f:
        f.write(advanced_readme)
    
    print("✅ Gelişmiş sürüm hazırlandı")

def copy_documentation(docs_dir):
    """Dokümantasyon kopyala"""
    print("\n📋 Dokümantasyon hazırlanıyor...")
    
    # Mevcut dokümantasyon dosyalarını kopyala
    docs_to_copy = [
        "README_FABRIKA_SISTEMI.md",
        "KURULUM_TAMAMLANDI.md"
    ]
    
    for doc in docs_to_copy:
        if os.path.exists(doc):
            shutil.copy2(doc, docs_dir)
            print(f"✅ Kopyalandı: {doc}")
    
    # Hızlı başlangıç rehberi
    quick_guide = """
🚀 HIZLI BAŞLANGIÇ REHBERİ
=========================

📋 SÜRÜM SEÇİMİ
===============

🔹 TEMEL SÜRÜM
-------------
✅ Basit ve hızlı kullanım
✅ Temel özellikler
✅ Kolay kurulum
❌ Yazıcı yönetimi yok
❌ Detaylı ayarlar yok

Kimler kullanmalı:
- İlk kez kullananlar
- Basit ihtiyaçları olanlar
- Hızlı başlamak isteyenler

🔹 GELİŞMİŞ SÜRÜM
-----------------
✅ Otomatik yazıcı algılama
✅ Yazıcı durum kontrolü
✅ Test yazdırma
✅ Detaylı log sistemi
✅ Gelişmiş ayarlar
✅ Sekmeli arayüz

Kimler kullanmalı:
- Detaylı kontrol isteyenler
- Birden fazla yazıcısı olanlar
- Gelişmiş özellik isteyenler

⚡ HIZLI KURULUM
===============

1️⃣ SÜRÜM SEÇ
- Temel kullanım → "1_Temel_Surum" klasörü
- Gelişmiş kullanım → "2_Gelismis_Surum" klasörü

2️⃣ BAŞLAT
- Temel: "Temel_Baslatma.bat" çalıştır
- Gelişmiş: "Gelismis_Baslatma.bat" çalıştır

3️⃣ AYARLA
- Bağlantı testi yap
- Yazıcı seç (gelişmiş sürümde)
- Sistemi başlat

4️⃣ KULLAN
- Artık siparişler otomatik yazdırılıyor!

🔧 SORUN ÇÖZME
==============
- Program açılmıyor → Windows Defender'ı kontrol et
- Yazıcı çalışmıyor → USB bağlantısını kontrol et
- Bağlantı yok → İnternet bağlantısını kontrol et

📞 YARDIM
=========
Detaylı bilgi için "3_Dokumantasyon" klasöründeki
dosyaları okuyun.
"""
    
    with open(os.path.join(docs_dir, "HIZLI_BASLANGIÇ.txt"), 'w', encoding='utf-8') as f:
        f.write(quick_guide)
    
    print("✅ Dokümantasyon hazırlandı")

def create_main_launchers(package_dir, basic_exists, advanced_exists):
    """Ana başlatma dosyaları oluştur"""
    print("\n📋 Ana başlatma dosyaları oluşturuluyor...")
    
    # Sürüm seçici
    selector_content = """@echo off
title Fabrika Yazici Sistemi - Surum Secici
cls
color 0F

echo.
echo  ===============================================
echo           TATO PASTA ^& BAKLAVA
echo         FABRİKA YAZICI SİSTEMİ
echo  ===============================================
echo.
echo  Hangi sürümü kullanmak istiyorsunuz?
echo.
"""
    
    if basic_exists:
        selector_content += """echo  [1] Temel Sürüm - Basit ve hızlı kullanım
echo      ✅ Kolay kullanım
echo      ✅ Temel özellikler
echo.
"""
    
    if advanced_exists:
        selector_content += """echo  [2] Gelişmiş Sürüm - Detaylı kontrol
echo      ✅ Otomatik yazıcı algılama
echo      ✅ Gelişmiş özellikler
echo      ✅ Detaylı ayarlar
echo.
"""
    
    selector_content += """echo  [0] Çıkış
echo.
set /p choice="Seçiminizi yapın: "

if "%choice%"=="0" exit
"""
    
    if basic_exists:
        selector_content += """
if "%choice%"=="1" (
    echo.
    echo  🚀 Temel sürüm başlatılıyor...
    cd "1_Temel_Surum"
    call "Temel_Baslatma.bat"
    cd ..
    goto end
)
"""
    
    if advanced_exists:
        selector_content += """
if "%choice%"=="2" (
    echo.
    echo  🚀 Gelişmiş sürüm başlatılıyor...
    cd "2_Gelismis_Surum"
    call "Gelismis_Baslatma.bat"
    cd ..
    goto end
)
"""
    
    selector_content += """
echo.
echo  ❌ Geçersiz seçim! Lütfen tekrar deneyin.
timeout /t 2 >nul
goto start

:end
echo.
echo  ✅ Program başlatıldı!
pause
"""
    
    # start: etiketi ekle
    selector_content = selector_content.replace("set /p choice=", ":start\nset /p choice=")
    
    with open(os.path.join(package_dir, "BAŞLAT.bat"), 'w', encoding='utf-8') as f:
        f.write(selector_content)
    
    print("✅ Ana başlatma dosyaları oluşturuldu")

def create_main_readme(package_dir, basic_exists, advanced_exists):
    """Ana README oluştur"""
    print("\n📋 Ana README oluşturuluyor...")
    
    readme_content = f"""
🏭 TATO PASTA & BAKLAVA - FABRİKA YAZICI SİSTEMİ
===============================================

📦 TAM KURULUM PAKETİ
====================

Bu pakette {'iki' if basic_exists and advanced_exists else 'bir'} farklı sürüm bulunmaktadır:

{'✅ TEMEL SÜRÜM - Basit ve hızlı kullanım' if basic_exists else ''}
{'✅ GELİŞMİŞ SÜRÜM - Detaylı kontrol ve yazıcı yönetimi' if advanced_exists else ''}

🚀 HIZLI BAŞLANGIÇ
=================

1️⃣ "BAŞLAT.bat" dosyasına çift tıklayın
2️⃣ Kullanmak istediğiniz sürümü seçin
3️⃣ Program otomatik olarak başlar

📁 PAKET İÇERİĞİ
===============
"""
    
    if basic_exists:
        readme_content += """
📂 1_Temel_Surum/
   🔧 FabrikaYaziciSistemi.exe
   ⚡ Temel_Baslatma.bat
   📄 TEMEL_SURUM_REHBERI.txt
"""
    
    if advanced_exists:
        readme_content += """
📂 2_Gelismis_Surum/
   🔧 GelismisFabrikaYazici.exe
   ⚡ Gelismis_Baslatma.bat
   📄 GELISMIS_SURUM_REHBERI.txt
"""
    
    readme_content += """
📂 3_Dokumantasyon/
   📋 HIZLI_BASLANGIÇ.txt
   📄 README_FABRIKA_SISTEMI.md
   📄 KURULUM_TAMAMLANDI.md

⚡ BAŞLAT.bat - Ana başlatma dosyası
📄 TAM_PAKET_REHBERİ.txt - Bu dosya

🎯 SÜRÜM SEÇİMİ
==============
"""
    
    if basic_exists:
        readme_content += """
🔹 TEMEL SÜRÜM
- Basit arayüz
- Temel yazdırma
- Hızlı kurulum
- Yeni başlayanlar için
"""
    
    if advanced_exists:
        readme_content += """
🔹 GELİŞMİŞ SÜRÜM
- Otomatik yazıcı algılama
- Yazıcı durum kontrolü
- Test yazdırma
- Detaylı log sistemi
- Gelişmiş kullanıcılar için
"""
    
    readme_content += """
🔧 SİSTEM GEREKSİNİMLERİ
=======================
- Windows 7/8/10/11
- En az 100 MB disk alanı
- İnternet bağlantısı
- USB veya ağ yazıcısı

📞 DESTEK
=========
Sorun yaşarsanız:
1. İlgili sürümün rehber dosyasını okuyun
2. Log dosyalarını kontrol edin
3. Sistem yöneticisiyle iletişime geçin

🎉 SİSTEM HAZIR!
===============
Artık şubelerden gelen siparişler
fabrikada otomatik yazdırılacak!
"""
    
    with open(os.path.join(package_dir, "TAM_PAKET_REHBERİ.txt"), 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ Ana README oluşturuldu")

def show_complete_package_contents(package_dir):
    """Tam paket içeriğini göster"""
    print(f"\n📁 TAM KURULUM PAKETİ İÇERİĞİ:")
    print("=" * 50)
    
    total_size = 0
    
    def show_directory(dir_path, indent=""):
        nonlocal total_size
        
        if not os.path.exists(dir_path):
            return
        
        for item in sorted(os.listdir(dir_path)):
            item_path = os.path.join(dir_path, item)
            
            if os.path.isfile(item_path):
                size = os.path.getsize(item_path)
                total_size += size
                
                if size > 1024 * 1024:  # MB
                    size_str = f"{size / (1024 * 1024):.1f} MB"
                elif size > 1024:  # KB
                    size_str = f"{size / 1024:.1f} KB"
                else:
                    size_str = f"{size} bytes"
                
                # Dosya türüne göre ikon
                if item.endswith('.exe'):
                    icon = "🔧"
                elif item.endswith('.bat'):
                    icon = "⚡"
                elif item.endswith('.txt'):
                    icon = "📄"
                elif item.endswith('.md'):
                    icon = "📋"
                else:
                    icon = "📁"
                
                print(f"{indent}{icon} {item:<35} {size_str:>10}")
            
            elif os.path.isdir(item_path):
                print(f"{indent}📂 {item}/")
                show_directory(item_path, indent + "   ")
    
    show_directory(package_dir)
    
    print("=" * 50)
    if total_size > 1024 * 1024:  # MB
        total_size_str = f"{total_size / (1024 * 1024):.1f} MB"
    else:  # KB
        total_size_str = f"{total_size / 1024:.1f} KB"
    
    print(f"📊 Toplam boyut: {total_size_str}")

def main():
    """Ana fonksiyon"""
    if create_complete_package():
        print(f"\n🎉 TAM KURULUM PAKETİ BAŞARIYLA OLUŞTURULDU!")
        
        print("\n📋 Fabrikaya kurulum için:")
        print("1. 'FabrikaYaziciSistemi_TAM_PAKET' klasörünü USB'ye kopyalayın")
        print("2. Fabrika bilgisayarında uygun bir yere yapıştırın")
        print("3. 'BAŞLAT.bat' dosyasını çalıştırın")
        print("4. İhtiyacınıza göre sürüm seçin")
        print("5. Bağlantı testini yapın ve sistemi başlatın")
        
        print("\n💡 Hangi sürümü seçmelisiniz?")
        print("   🔹 Temel Sürüm: İlk kez kullananlar, basit ihtiyaçlar")
        print("   🔹 Gelişmiş Sürüm: Detaylı kontrol, yazıcı yönetimi")
    else:
        print("\n❌ Paket oluşturulamadı!")

if __name__ == "__main__":
    main()