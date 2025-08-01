#!/usr/bin/env python3
"""
Fabrika kurulum paketi oluşturucu
"""

import os
import shutil
from pathlib import Path

def create_installation_package():
    """Fabrika kurulum paketi oluştur"""
    
    print("📦 Fabrika Yazıcı Sistemi - Kurulum Paketi Oluşturucu")
    print("=" * 60)
    
    # EXE dosyasını kontrol et
    exe_path = "dist/FabrikaYaziciSistemi.exe"
    if not os.path.exists(exe_path):
        print(f"❌ EXE dosyası bulunamadı: {exe_path}")
        print("💡 Önce: python -m PyInstaller --onefile --windowed --name=FabrikaYaziciSistemi fabrika_yazici_program.py")
        return False
    
    # Dosya boyutunu kontrol et
    file_size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
    print(f"✅ EXE dosyası bulundu: {exe_path}")
    print(f"📊 Dosya boyutu: {file_size:.1f} MB")
    
    # Kurulum klasörü oluştur
    package_dir = "FabrikaYaziciSistemi_Kurulum"
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
        print(f"🗑️  Eski klasör temizlendi: {package_dir}")
    
    os.makedirs(package_dir)
    print(f"📁 Kurulum klasörü oluşturuldu: {package_dir}")
    
    # 1. EXE dosyasını kopyala
    shutil.copy2(exe_path, package_dir)
    print(f"✅ EXE kopyalandı")
    
    # 2. README dosyasını kopyala
    if os.path.exists("README_FABRIKA_SISTEMI.md"):
        shutil.copy2("README_FABRIKA_SISTEMI.md", package_dir)
        print("✅ README kopyalandı")
    
    # 3. Kurulum rehberi oluştur
    create_installation_guide(package_dir)
    
    # 4. Başlatma scripti oluştur
    create_startup_script(package_dir)
    
    # 5. Test scripti oluştur
    create_test_script(package_dir)
    
    # 6. Destek dosyaları oluştur
    create_support_files(package_dir)
    
    # Paket içeriğini göster
    show_package_contents(package_dir)
    
    print(f"\n🎉 Kurulum paketi hazır!")
    print(f"📂 Konum: {os.path.abspath(package_dir)}")
    print("\n📋 Sonraki adımlar:")
    print("1. Bu klasörü fabrika bilgisayarına kopyalayın")
    print("2. 'Baslatma.bat' dosyasını çalıştırın")
    print("3. Veya 'FabrikaYaziciSistemi.exe' dosyasına çift tıklayın")
    
    return True

def create_installation_guide(package_dir):
    """Detaylı kurulum rehberi oluştur"""
    
    guide_content = """
🏭 TATO PASTA & BAKLAVA - FABRİKA YAZICI SİSTEMİ
===============================================

📋 KURULUM REHBERİ
==================

🎯 HIZLI BAŞLANGIÇ
-----------------
1. 'Baslatma.bat' dosyasına çift tıklayın
2. Program otomatik olarak açılacak
3. "🔍 Bağlantı Testi" butonuna tıklayın
4. "▶️ Başlat" butonuna tıklayın
5. Artık siparişler otomatik yazdırılacak!

⚙️ SİSTEM GEREKSİNİMLERİ
------------------------
- Windows 7/8/10/11 (32-bit veya 64-bit)
- En az 100 MB boş disk alanı
- İnternet bağlantısı (sürekli)
- USB veya ağ yazıcısı

📥 KURULUM ADIMLARI
------------------

Adım 1: Dosyaları Yerleştirme
- Bu klasörü fabrika bilgisayarında uygun bir yere kopyalayın
- Önerilen konum: C:\FabrikaYazici\

Adım 2: İlk Çalıştırma
- 'Baslatma.bat' dosyasına çift tıklayın
- VEYA 'FabrikaYaziciSistemi.exe' dosyasına çift tıklayın

Adım 3: Güvenlik Uyarısı
- Windows "Bilinmeyen yayımcı" uyarısı verebilir
- "Ek bilgi" → "Yine de çalıştır" seçin
- Bu normal bir durumdur

Adım 4: İlk Ayarlar
- Program açıldığında "🔍 Bağlantı Testi" butonuna tıklayın
- Yeşil "🟢 Bağlı" yazısını görene kadar bekleyin
- "▶️ Başlat" butonuna tıklayın

🖥️ PROGRAM KULLANIMI
--------------------

Ana Ekran Açıklaması:
- 🟢 Bağlı: İnternet bağlantısı var
- 🔴 Bağlantı Yok: İnternet sorunu
- ▶️ Çalışıyor: Sistem aktif, sipariş dinliyor
- ⏸️ Durduruldu: Sistem pasif

Butonlar:
- ▶️ Başlat: Sipariş dinlemeyi başlat
- ⏹️ Durdur: Sipariş dinlemeyi durdur
- 🔍 Bağlantı Testi: İnternet bağlantısını test et
- 🔄 Yenile: Manuel sipariş kontrolü yap
- ⚙️ Ayarlar: Gelişmiş ayarlar

Tablolar:
- Üst tablo: Gelen siparişler listesi
- Alt alan: Program aktivite logu

🖨️ YAZICI AYARLARI
------------------

Desteklenen Yazıcılar:
- USB bağlantılı termal yazıcılar
- Ağ yazıcıları (IP üzerinden)
- Windows varsayılan yazıcısı

Yazıcı Hazırlığı:
1. Yazıcının açık ve hazır olduğundan emin olun
2. Kağıt yüklenmiş olmalı
3. Windows'ta yazıcı tanımlı olmalı

Test Yazdırma:
- 'TestYazdirma.bat' dosyasını çalıştırın
- Test çıktısı geliyorsa yazıcı hazır

🔧 SORUN GİDERME
---------------

Program Açılmıyor:
□ Windows Defender'ı geçici olarak kapatın
□ Dosyaya sağ tık → "Yönetici olarak çalıştır"
□ Antivirüs programını kontrol edin

Bağlantı Sorunu:
□ İnternet bağlantınızı test edin
□ Firewall ayarlarını kontrol edin
□ Ayarlarda API URL'sini kontrol edin

Yazıcı Çalışmıyor:
□ Yazıcının açık olduğunu kontrol edin
□ USB kablosunu kontrol edin
□ Windows'ta yazıcı durumunu kontrol edin
□ Test yazdırma yapın

Program Yavaş:
□ İnternet hızınızı test edin
□ Kontrol aralığını artırın (Ayarlar)
□ Gereksiz programları kapatın

📊 VARSAYILAN AYARLAR
--------------------
- API URL: https://siparis.tatopastabaklava.com
- Güvenlik Token: factory_printer_2024
- Kontrol Aralığı: 30 saniye
- Yazıcı: Windows varsayılan yazıcısı

📞 DESTEK VE YARDIM
------------------

Log Dosyaları:
- Ana log: fabrika_log.txt
- Yazdırılan siparişler: yazdirilanlar/ klasörü

Hata Durumunda:
1. fabrika_log.txt dosyasını açın
2. En son hata mesajlarını not alın
3. Sistem yöneticisine iletin

İletişim:
- Sistem Yöneticisi: [İletişim bilgileri]
- Teknik Destek: [Destek hattı]

📈 PERFORMANS TAVSİYELERİ
-------------------------
- Program sürekli açık tutun
- Bilgisayarı uyku moduna almayın
- İnternet bağlantısını stabil tutun
- Yazıcı kağıdını kontrol edin
- Günlük log dosyalarını kontrol edin

🔄 GÜNCELLEME
------------
- Yeni sürümler çıktığında size bildirilecek
- Eski kurulumu silin, yeni dosyaları kopyalayın
- Ayarlar otomatik olarak korunur

⚡ ACİL DURUM
------------
Program çöktüğünde:
1. Programı kapatın (Task Manager'dan)
2. 'Baslatma.bat' ile yeniden başlatın
3. Log dosyasını kontrol edin

Yazıcı durduğunda:
1. Yazıcıyı yeniden başlatın
2. Test yazdırma yapın
3. Program otomatik devam edecek

===============================================
🎉 Sistem kullanıma hazır!
Sorularınız için sistem yöneticisiyle iletişime geçin.
"""
    
    with open(os.path.join(package_dir, "KURULUM_REHBERİ.txt"), 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print("✅ Kurulum rehberi oluşturuldu")

def create_startup_script(package_dir):
    """Başlatma scripti oluştur"""
    
    bat_content = """@echo off
title Fabrika Yazici Sistemi Başlatıcı
cls
color 0A

echo.
echo  ===============================================
echo            TATO PASTA ^& BAKLAVA
echo         FABRİKA YAZICI SİSTEMİ
echo  ===============================================
echo.
echo  📋 Program başlatılıyor...
echo.

REM Geçerli dizini belirle
cd /d "%~dp0"

REM EXE dosyasının varlığını kontrol et
if exist "FabrikaYaziciSistemi.exe" (
    echo  ✅ Program dosyası bulundu
    echo.
    echo  🚀 Yazıcı sistemi başlatılıyor...
    echo.
    
    REM 2 saniye bekle
    timeout /t 2 /nobreak >nul
    
    REM Programı başlat
    start "" "FabrikaYaziciSistemi.exe"
    
    echo  ✅ Program başlatıldı!
    echo.
    echo  📝 Şimdi yapmanız gerekenler:
    echo     1. Bağlantı testini yapın
    echo     2. 'Başlat' butonuna tıklayın
    echo     3. Sistemin siparişleri dinlemesini bekleyin
    echo.
    echo  💡 Bu pencereyi kapatabilirsiniz.
    echo.
    pause
    
) else (
    echo  ❌ HATA: FabrikaYaziciSistemi.exe bulunamadı!
    echo.
    echo  📁 Bu dosyanın bulunduğu klasörde olması gereken dosyalar:
    echo     - FabrikaYaziciSistemi.exe
    echo     - Baslatma.bat (bu dosya)
    echo     - KURULUM_REHBERİ.txt
    echo.
    echo  💡 Dosyaları doğru klasöre kopyaladığınızdan emin olun.
    echo.
    pause
)
"""
    
    with open(os.path.join(package_dir, "Baslatma.bat"), 'w', encoding='utf-8') as f:
        f.write(bat_content)
    
    print("✅ Başlatma scripti oluşturuldu")

def create_test_script(package_dir):
    """Test scripti oluştur"""
    
    test_content = """@echo off
title Yazıcı Test Programı
cls
color 0B

echo.
echo  ===============================================
echo            YAZICI TEST PROGRAMI
echo  ===============================================
echo.
echo  🖨️  Yazıcı bağlantısı test ediliyor...
echo.

REM Test metni oluştur
echo Test yazdırma - %date% %time% > test_ciktisi.txt
echo. >> test_ciktisi.txt
echo TATO PASTA ^& BAKLAVA >> test_ciktisi.txt
echo Fabrika Yazıcı Sistemi >> test_ciktisi.txt
echo. >> test_ciktisi.txt
echo Bu bir test çıktısıdır. >> test_ciktisi.txt
echo Eğer bu metni görebiliyorsanız >> test_ciktisi.txt
echo yazıcınız çalışıyor demektir. >> test_ciktisi.txt
echo. >> test_ciktisi.txt
echo Test tarihi: %date% >> test_ciktisi.txt
echo Test saati: %time% >> test_ciktisi.txt

REM Varsayılan yazıcıya gönder
echo  📄 Test dosyası oluşturuldu: test_ciktisi.txt
echo.
echo  🖨️  Varsayılan yazıcıya gönderiliyor...

print test_ciktisi.txt

echo.
echo  ✅ Test tamamlandı!
echo.
echo  📋 Sonuç:
echo     - Yazıcıdan çıktı aldıysanız: Yazıcı hazır ✅
echo     - Çıktı alamadıysanız: Yazıcı ayarlarını kontrol edin ❌
echo.
echo  💡 Sorun yaşıyorsanız:
echo     1. Yazıcının açık olduğunu kontrol edin
echo     2. USB bağlantısını kontrol edin  
echo     3. Windows yazıcı ayarlarını kontrol edin
echo.
pause
"""
    
    with open(os.path.join(package_dir, "TestYazdirma.bat"), 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    print("✅ Test scripti oluşturuldu")

def create_support_files(package_dir):
    """Destek dosyaları oluştur"""
    
    # Hızlı başlangıç kılavuzu
    quick_start = """
🚀 HIZLI BAŞLANGIÇ
=================

1️⃣ 'Baslatma.bat' dosyasına çift tıklayın

2️⃣ Program açıldığında "🔍 Bağlantı Testi" yapın

3️⃣ "▶️ Başlat" butonuna tıklayın

4️⃣ Artık siparişler otomatik yazdırılıyor! 🎉

❓ Sorun mu var?
- 'KURULUM_REHBERİ.txt' dosyasını okuyun
- 'TestYazdirma.bat' ile yazıcıyı test edin

📞 Yardım: Sistem yöneticisiyle iletişime geçin
"""
    
    with open(os.path.join(package_dir, "HIZLI_BAŞLANGIÇ.txt"), 'w', encoding='utf-8') as f:
        f.write(quick_start)
    
    # Sorun giderme rehberi
    troubleshooting = """
🔧 SORUN GİDERME REHBERİ
=======================

🔴 PROGRAM AÇILMIYOR
-------------------
□ Windows Defender'ı geçici olarak kapatın
□ Dosyaya sağ tık → "Yönetici olarak çalıştır"
□ Antivirüs programının engellemediğini kontrol edin

🔴 BAĞLANTI SORUNU
-----------------
□ İnternet bağlantınızı test edin (chrome açıp site ziyaret edin)
□ Firewall'un programı engellemediğini kontrol edin
□ Şirket ağındaysanız IT departmanıyla konuşun

🔴 YAZICI ÇALIŞMIYOR
-------------------
□ Yazıcının açık ve hazır olduğunu kontrol edin
□ USB kablosunu çıkarıp takın
□ 'TestYazdirma.bat' ile test yapın
□ Windows'ta Yazıcılar'dan durumu kontrol edin

🔴 SİPARİŞ GELMİYOR
------------------
□ "▶️ Başlat" butonuna bastığınızı kontrol edin
□ Yeşil "🟢 Bağlı" yazısının görünür olduğunu kontrol edin
□ "🔄 Yenile" butonuyla manuel kontrol yapın

🔴 PROGRAM DONUYOR
-----------------
□ Task Manager'dan programı kapatın
□ 'Baslatma.bat' ile yeniden başlatın
□ Bilgisayarı yeniden başlatın

📞 ACİL YARDIM
-------------
1. fabrika_log.txt dosyasını açın
2. En son satırlardaki hata mesajını kopyalayın
3. Sistem yöneticisiyle paylaşın
"""
    
    with open(os.path.join(package_dir, "SORUN_GİDERME.txt"), 'w', encoding='utf-8') as f:
        f.write(troubleshooting)
    
    print("✅ Destek dosyaları oluşturuldu")

def show_package_contents(package_dir):
    """Paket içeriğini göster"""
    
    print(f"\n📁 Kurulum Paketi İçeriği:")
    print("=" * 40)
    
    total_size = 0
    for file in sorted(os.listdir(package_dir)):
        file_path = os.path.join(package_dir, file)
        if os.path.isfile(file_path):
            size = os.path.getsize(file_path)
            total_size += size
            
            if size > 1024 * 1024:  # MB
                size_str = f"{size / (1024 * 1024):.1f} MB"
            elif size > 1024:  # KB
                size_str = f"{size / 1024:.1f} KB"
            else:  # Bytes
                size_str = f"{size} bytes"
            
            # Dosya türüne göre ikon
            if file.endswith('.exe'):
                icon = "🔧"
            elif file.endswith('.bat'):
                icon = "⚡"
            elif file.endswith('.txt'):
                icon = "📄"
            elif file.endswith('.md'):
                icon = "📋"
            else:
                icon = "📁"
            
            print(f"   {icon} {file:<30} {size_str:>10}")
    
    print("=" * 40)
    if total_size > 1024 * 1024:  # MB
        total_size_str = f"{total_size / (1024 * 1024):.1f} MB"
    else:  # KB
        total_size_str = f"{total_size / 1024:.1f} KB"
    
    print(f"   📊 Toplam boyut: {total_size_str}")

def main():
    """Ana fonksiyon"""
    
    if create_installation_package():
        print(f"\n🎉 Kurulum paketi başarıyla oluşturuldu!")
        
        print("\n📋 Fabrikaya kurulum için:")
        print("1. 'FabrikaYaziciSistemi_Kurulum' klasörünü USB'ye kopyalayın")
        print("2. Fabrika bilgisayarında uygun bir yere yapıştırın")
        print("3. 'HIZLI_BAŞLANGIÇ.txt' dosyasını okuyun")
        print("4. 'Baslatma.bat' dosyasını çalıştırın")
        
        print("\n💡 İpucu: Kurulum öncesi yazıcının hazır olduğundan emin olun!")
    else:
        print("\n❌ Kurulum paketi oluşturulamadı!")

if __name__ == "__main__":
    main()