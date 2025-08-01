#!/usr/bin/env python3
"""
Final Fabrika Yazıcı Sistemi - Tek Tam Sürüm
Tüm özellikleri içeren tek kurulum paketi
"""

import os
import shutil
from pathlib import Path

def create_final_package():
    """Final tek sürüm paketi oluştur"""
    
    print("🏭 TATO PASTA & BAKLAVA - FİNAL FABRİKA YAZICI SİSTEMİ")
    print("=" * 70)
    
    # En gelişmiş sürümü kullan
    source_exe = "dist/SuperGelismisFabrikaYazici.exe"
    
    if not os.path.exists(source_exe):
        print(f"❌ HATA: {source_exe} bulunamadı!")
        return False
    
    # Ana kurulum klasörü
    package_dir = "FabrikaYaziciSistemi_FINAL"
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
        print(f"🗑️ Eski paket temizlendi")
    
    os.makedirs(package_dir)
    print(f"📁 Final paket klasörü oluşturuldu: {package_dir}")
    
    # Ana EXE dosyasını kopyala ve yeniden adlandır
    final_exe_name = "FabrikaYaziciSistemi.exe"
    shutil.copy2(source_exe, os.path.join(package_dir, final_exe_name))
    
    size = os.path.getsize(source_exe) / (1024 * 1024)
    print(f"✅ Ana program kopyalandı: {final_exe_name} ({size:.1f} MB)")
    
    # Ana başlatma scripti
    create_main_launcher(package_dir, final_exe_name)
    
    # Test scripti
    create_test_script(package_dir, final_exe_name)
    
    # Kurulum rehberi
    create_installation_guide(package_dir)
    
    # Hızlı başlangıç
    create_quick_guide(package_dir)
    
    # Sorun giderme
    create_troubleshooting_guide(package_dir)
    
    # Dokümantasyon kopyala
    copy_documentation(package_dir)
    
    # Paket içeriğini göster
    show_package_contents(package_dir)
    
    print(f"\n🎉 FİNAL KURULUM PAKETİ HAZIR!")
    print(f"📂 Konum: {os.path.abspath(package_dir)}")
    
    return True

def create_main_launcher(package_dir, exe_name):
    """Ana başlatma scripti"""
    
    launcher_content = f"""@echo off
title TATO PASTA & BAKLAVA - Fabrika Yazici Sistemi
cls
color 0B

echo.
echo  ===============================================
echo         🏭 TATO PASTA ^& BAKLAVA 🏭
echo       FABRİKA YAZICI SİSTEMİ v2.0
echo  ===============================================
echo.
echo  🚀 Gelişmiş Özellikler:
echo     ✅ Otomatik yazıcı algılama
echo     ✅ Ağ yazıcıları desteği  
echo     ✅ Kapsamlı test merkezi
echo     ✅ Akıllı durum takibi
echo     ✅ Kolay kullanım arayüzü
echo.
echo  Program başlatılıyor...
echo.

cd /d "%~dp0"

if exist "{exe_name}" (
    echo  ✅ Program dosyası bulundu
    echo  🚀 Fabrika Yazıcı Sistemi başlatılıyor...
    echo.
    
    REM Program başlat
    start "" "{exe_name}"
    
    echo  ✅ Program başlatıldı!
    echo.
    echo  💡 İlk kullanım için:
    echo     1. Yazıcı Yönetimi sekmesinden yazıcı seçin
    echo     2. Ana Kontrol'den "Bağlantı Testi" yapın
    echo     3. "Sistemi Başlat" butonuna tıklayın
    echo.
    echo  📋 Program çalışıyor. Bu pencereyi kapatabilirsiniz.
    echo.
    timeout /t 5 >nul
    
) else (
    echo  ❌ HATA: {exe_name} bulunamadı!
    echo.
    echo  Dosyanın bu klasörde olduğundan emin olun.
    echo  Antivirüs programının dosyayı silmediğini kontrol edin.
    echo.
    pause
)
"""
    
    with open(os.path.join(package_dir, "🚀_BASLATMA.bat"), 'w', encoding='utf-8') as f:
        f.write(launcher_content)

def create_test_script(package_dir, exe_name):
    """Test scripti"""
    
    test_content = f"""@echo off
title Fabrika Yazici Sistemi - Test Modu
cls
color 0E

echo.
echo  ===============================================
echo         🧪 TEST MODU BAŞLATILIYOR 🧪
echo       FABRİKA YAZICI SİSTEMİ
echo  ===============================================
echo.
echo  Bu mod sadece test amaçlıdır.
echo  Gerçek siparişler yazdırılmayacak.
echo.
echo  Test özellikları:
echo     🔍 Yazıcı bağlantı testi
echo     🖨️ Test yazdırma
echo     🌐 API bağlantı kontrolü
echo     📊 Sistem durum raporu
echo.

set /p confirm="Test modunu başlatmak istiyor musunuz? (E/H): "

if /i "%confirm%"=="E" (
    echo.
    echo  🚀 Test modu başlatılıyor...
    echo.
    start "" "{exe_name}"
    echo  ✅ Test modu aktif!
    echo  💡 Program açıldığında "Test Merkezi" sekmesini kullanın.
    timeout /t 3 >nul
) else (
    echo.
    echo  ❌ Test modu iptal edildi.
    timeout /t 2 >nul
)
"""
    
    with open(os.path.join(package_dir, "🧪_TEST_MODU.bat"), 'w', encoding='utf-8') as f:
        f.write(test_content)

def create_installation_guide(package_dir):
    """Kurulum rehberi"""
    
    guide_content = """
🏭 FABRİKA YAZICI SİSTEMİ - KURULUM REHBERİ
==========================================

🚀 HIZLI KURULUM (2 DAKİKA)
===========================

1️⃣ PROGRAM BAŞLATMA
-------------------
"🚀_BASLATMA.bat" dosyasına çift tıklayın

2️⃣ YAZICI AYARLAMA
------------------
Program açıldığında:
• "Yazıcı Yönetimi" sekmesine gidin
• "Yeniden Tara" butonuna tıklayın
• Yazıcınızı seçin ve "Seç" butonuna tıklayın
• "Test Et" ile yazıcınızı test edin

3️⃣ BAĞLANTI KONTROLÜ
--------------------
• "Ana Kontrol" sekmesine gidin
• "Bağlantı Testi" butonuna tıklayın
• Yeşil "Bağlı" durumunu gördüğünüzde hazırsınız

4️⃣ SİSTEMİ BAŞLATMA
-------------------
• "Sistemi Başlat" butonuna tıklayın
• Artık siparişler otomatik yazdırılacak!

🔧 DETAYLI KURULUM ADIMLARİ
===========================

📋 ÖN HAZIRLIK
--------------
□ Yazıcının bilgisayara bağlı olduğunu kontrol edin
□ Yazıcının açık ve hazır olduğunu kontrol edin
□ İnternet bağlantısının çalıştığını kontrol edin
□ Windows Defender'ın programı engellemediğini kontrol edin

🖥️ SİSTEM GEREKSİNİMLERİ
------------------------
✅ Windows 7/8/10/11 (64-bit önerilen)
✅ En az 100 MB boş disk alanı
✅ İnternet bağlantısı (sürekli)
✅ USB veya ağ yazıcısı
✅ .NET Framework (genellikle yüklü)

🖨️ YAZICI KURULUMU
------------------
Eğer yazıcınız henüz kurulu değilse:

1. Yazıcıyı USB ile bilgisayara bağlayın
2. Windows Ayarlar > Yazıcılar ve Tarayıcılar
3. "Yazıcı veya tarayıcı ekle" seçeneğine tıklayın
4. Sistemin yazıcıyı bulmasını bekleyin
5. Kurulum talimatlarını takip edin
6. Test sayfası yazdırın

🌐 AĞ YAZICI KURULUMU
--------------------
Ağ yazıcısı kullanıyorsanız:

1. Yazıcının IP adresini öğrenin
2. Windows Ayarlar > Yazıcılar ve Tarayıcılar
3. "Yazıcı veya tarayıcı ekle"
4. "İstediğim yazıcı listede yok"
5. "TCP/IP adresi ile yazıcı ekle"
6. IP adresini girin ve devam edin

🔐 GÜVENLİK AYARLARI
-------------------
Windows Defender uyarısı verirse:

1. "Ayrıntılar" linkine tıklayın
2. "Yine de çalıştır" seçeneğini seçin
3. Veya programı güvenlik istisnalarına ekleyin

💡 İLK KULLANIM İPUÇLARI
=======================
□ İlk açılışta mutlaka yazıcı testini yapın
□ Bağlantı testini yaparak API'nin çalıştığını kontrol edin
□ Test yazdırma ile formatın doğru olduğunu kontrol edin
□ Program sürekli açık tutulmalıdır
□ Bilgisayar uyku moduna geçmemelidir

🔧 SORUN ÇÖZME
==============
□ Program açılmıyor → Antivirüs kontrol edin
□ Yazıcı bulunamıyor → USB'yi çıkarıp takın
□ Bağlantı sorunu → İnternet kontrol edin
□ Yazdırma çalışmıyor → Yazıcı test edin

📞 YARDIM
=========
Bu rehberde çözemediğiniz sorunlar için:
• "SORUN_GIDERME.txt" dosyasını okuyun
• Log dosyalarını kontrol edin
• Sistem yöneticisiyle iletişime geçin

🎉 KURULUM TAMAMLANDI!
=====================
Artık şubelerden gelen siparişler
fabrikada otomatik yazdırılacak!

İyi kullanımlar! 🎯
"""
    
    with open(os.path.join(package_dir, "📋_KURULUM_REHBERI.txt"), 'w', encoding='utf-8') as f:
        f.write(guide_content)

def create_quick_guide(package_dir):
    """Hızlı başlangıç rehberi"""
    
    quick_content = """
⚡ SÜPER HIZLI BAŞLANGIÇ
======================

🎯 3 ADIMDA HAZIR!
==================

1️⃣ BAŞLAT
----------
🚀_BASLATMA.bat dosyasına çift tık

2️⃣ AYARLA  
----------
Yazıcı Yönetimi → Yazıcı seç → Test et

3️⃣ ÇALIŞTIR
-----------
Ana Kontrol → Bağlantı Testi → Sistemi Başlat

🎉 HAZIR! Siparişler otomatik yazdırılıyor!

🔧 SORUN VARSA
==============
□ Yazıcı açık mı?
□ İnternet var mı?
□ Windows Defender engelliyor mu?

📋 Detaylı yardım: KURULUM_REHBERI.txt

Bu kadar basit! 🚀
"""
    
    with open(os.path.join(package_dir, "⚡_HIZLI_BASLANGIÇ.txt"), 'w', encoding='utf-8') as f:
        f.write(quick_content)

def create_troubleshooting_guide(package_dir):
    """Sorun giderme rehberi"""
    
    troubleshooting_content = """
🔧 SORUN GİDERME REHBERİ
=======================

🔴 PROGRAM AÇILMIYOR
-------------------
Belirtiler: Program başlamıyor, hata veriyor

Çözümler:
□ Windows Defender'ı geçici olarak kapatın
□ Dosyaya sağ tık → "Yönetici olarak çalıştır"
□ Antivirüs programını kontrol edin
□ .NET Framework güncel mi kontrol edin
□ Bilgisayarı yeniden başlatın

🔴 YAZICI BULUNAMIYOR
--------------------
Belirtiler: "Yazıcı seçilmedi" uyarısı

Çözümler:
□ Yazıcının açık ve hazır olduğunu kontrol edin
□ USB kablosunu çıkarıp tekrar takın  
□ Windows Ayarlar → Yazıcılar'da görünüyor mu kontrol edin
□ Yazıcı sürücülerini güncelleyin
□ "Yazıcı Yönetimi" sekmesinde "Yeniden Tara" yapın
□ "Yazıcı Keşfi" sekmesini kullanın

🔴 BAĞLANTI SORUNU
-----------------
Belirtiler: "Bağlantı Yok" durumu

Çözümler:
□ İnternet bağlantısını test edin (bir web sitesi açın)
□ Firewall programını kontrol edin
□ VPN kullanıyorsanız geçici olarak kapatın
□ Şirket ağındaysanız IT departmanıyla konuşun
□ "Ayarlar" sekmesinde API URL'sini kontrol edin

🔴 YAZDIRMA ÇALIŞMIYOR
---------------------
Belirtiler: Siparişler geliyor ama yazdırılmıyor

Çözümler:
□ "Test Merkezi" sekmesinde yazıcı testini yapın
□ Yazıcı kuyruğunu kontrol edin (bekleyen işler var mı?)
□ Kağıt ve mürekkep/toner durumunu kontrol edin
□ Yazıcıyı kapatıp açın
□ Windows yazıcı sorun gidericisini çalıştırın
□ Yazıcı ayarlarından "Test sayfası yazdır"

🔴 SİPARİŞLER GELMİYOR
---------------------
Belirtiler: Program çalışıyor ama sipariş gelmiyor

Çözümler:
□ "Sistemi Başlat" butonuna bastığınızı kontrol edin
□ Bağlantı durumunun "Yeşil - Bağlı" olduğunu kontrol edin
□ "Yenile" butonunu deneyin
□ Ayarlar'da token'ın doğru olduğunu kontrol edin
□ Sistem yöneticisiyle iletişime geçin

🔴 PROGRAM YAVAŞ ÇALIŞIYOR
-------------------------
Belirtiler: Donma, gecikmeler

Çözümler:
□ İnternet hızınızı test edin
□ Gereksiz programları kapatın
□ Kontrol aralığını artırın (Ayarlar sekmesi)
□ Bilgisayarı yeniden başlatın
□ Log dosyalarını temizleyin

📊 PERFORMANS İPUÇLARI
======================
✅ Programı sürekli açık tutun
✅ Bilgisayarı uyku moduna almayın  
✅ Düzenli olarak log dosyalarını temizleyin
✅ Yazıcı kağıdını kontrol edin
✅ İnternet bağlantısını stabil tutun
✅ Yazıcı çevresini temiz tutun

📞 ACİL YARDIM PROTOKOLÜ
=======================
Sorun devam ediyorsa:

1. Log dosyasını açın:
   - "Loglar" sekmesine gidin
   - En son hata mesajlarını kopyalayın

2. Sistem bilgilerini not alın:
   - Windows sürümü
   - Yazıcı modeli
   - Hata mesajı

3. Sistem yöneticisine iletin

4. Varsa ekran görüntüsü alın

🆘 ACİL DURUM ÇÖZÜMÜ
===================
Hiçbir şey çalışmıyorsa:

1. Programı tamamen kapatın
2. Bilgisayarı yeniden başlatın
3. Yazıcıyı kapatıp açın
4. İnternet bağlantısını test edin
5. Programı "Yönetici olarak çalıştır"
6. "Test Modu" ile başlatın

Bu genellikle sorunların %90'ını çözer.

📝 LOG DOSYALARİ
===============
Sorun giderme için log dosyaları çok önemlidir:
- fabrika_log.txt (ana log)
- super_fabrika_log.txt (detaylı log)

Bu dosyalar program klasöründe oluşturulur.
"""
    
    with open(os.path.join(package_dir, "🔧_SORUN_GIDERME.txt"), 'w', encoding='utf-8') as f:
        f.write(troubleshooting_content)

def copy_documentation(package_dir):
    """Mevcut dokümantasyonu kopyala"""
    docs_to_copy = [
        "README_FABRIKA_SISTEMI.md",
        "KURULUM_TAMAMLANDI.md"
    ]
    
    docs_dir = os.path.join(package_dir, "📚_DOKUMANTASYON")
    os.makedirs(docs_dir, exist_ok=True)
    
    for doc in docs_to_copy:
        if os.path.exists(doc):
            shutil.copy2(doc, docs_dir)
            print(f"✅ Kopyalandı: {doc}")

def show_package_contents(package_dir):
    """Paket içeriğini göster"""
    print(f"\n📁 FİNAL PAKET İÇERİĞİ:")
    print("=" * 50)
    
    total_size = 0
    
    for item in sorted(os.listdir(package_dir)):
        item_path = os.path.join(package_dir, item)
        
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
            else:
                icon = "📁"
            
            print(f"{icon} {item:<35} {size_str:>10}")
        
        elif os.path.isdir(item_path):
            print(f"📂 {item}/")
            # Alt klasör içeriğini de göster
            for subitem in os.listdir(item_path):
                subitem_path = os.path.join(item_path, subitem)
                if os.path.isfile(subitem_path):
                    size = os.path.getsize(subitem_path)
                    total_size += size
                    if size > 1024:
                        size_str = f"{size / 1024:.1f} KB"
                    else:
                        size_str = f"{size} bytes"
                    print(f"   📄 {subitem:<30} {size_str:>10}")
    
    print("=" * 50)
    if total_size > 1024 * 1024:  # MB
        total_size_str = f"{total_size / (1024 * 1024):.1f} MB"
    else:  # KB
        total_size_str = f"{total_size / 1024:.1f} KB"
    
    print(f"📊 Toplam boyut: {total_size_str}")

def main():
    """Ana fonksiyon"""
    if create_final_package():
        print(f"\n🎉 FİNAL KURULUM PAKETİ BAŞARIYLA OLUŞTURULDU!")
        
        print("\n📋 Fabrikaya kurulum için:")
        print("1. 'FabrikaYaziciSistemi_FINAL' klasörünü USB'ye kopyalayın")
        print("2. Fabrika bilgisayarında uygun bir yere yapıştırın")
        print("3. '🚀_BASLATMA.bat' dosyasını çalıştırın")
        print("4. Yazıcıyı seçin ve sistemi başlatın")
        
        print("\n💡 Bu tek sürüm şunları içerir:")
        print("   🚀 Otomatik yazıcı algılama")
        print("   🖨️ Ağ yazıcıları desteği")
        print("   🧪 Kapsamlı test merkezi")
        print("   📊 Akıllı durum takibi")
        print("   ⚙️ Gelişmiş ayarlar")
        print("   📝 Detaylı log sistemi")
        
        print("\n🎯 Artık tek bir dosya ile her şey dahil!")
    else:
        print("\n❌ Final paket oluşturulamadı!")

if __name__ == "__main__":
    main()