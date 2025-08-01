#!/usr/bin/env python3
"""
ÇALIŞAN Fabrika Yazıcı Sistemi - Final Paket
Gerçek işlevsellikli tek kurulum paketi
"""

import os
import shutil
from pathlib import Path

def create_working_package():
    """Çalışan final paket oluştur"""
    
    print("🏭 TATO PASTA & BAKLAVA - ÇALIŞAN FABRİKA YAZICI SİSTEMİ")
    print("=" * 70)
    
    # Çalışan sürümü kullan
    source_exe = "dist/FabrikaYaziciSistemi_CALISIR.exe"
    
    if not os.path.exists(source_exe):
        print(f"❌ HATA: {source_exe} bulunamadı!")
        return False
    
    # Ana kurulum klasörü
    package_dir = "FabrikaYaziciSistemi_CALISIR_FINAL"
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
    
    # Hızlı başlangıç
    create_quick_guide(package_dir)
    
    # Detaylı rehber
    create_detailed_guide(package_dir)
    
    # Paket içeriğini göster
    show_package_contents(package_dir)
    
    print(f"\n🎉 ÇALIŞAN FİNAL KURULUM PAKETİ HAZIR!")
    print(f"📂 Konum: {os.path.abspath(package_dir)}")
    
    return True

def create_main_launcher(package_dir, exe_name):
    """Ana başlatma scripti"""
    
    launcher_content = f"""@echo off
title TATO PASTA & BAKLAVA - CALISIR Fabrika Yazici Sistemi
cls
color 0A

echo.
echo  ===============================================
echo         🏭 TATO PASTA ^& BAKLAVA 🏭
echo       ÇALIŞAN FABRİKA YAZICI SİSTEMİ
echo  ===============================================
echo.
echo  ✅ Bu sürümde TÜM BUTONLAR ÇALIŞIR!
echo.
echo  🚀 Çalışan Özellikler:
echo     ✅ Yazıcı tarama ve seçimi
echo     ✅ Gerçek test yazdırmaları
echo     ✅ API bağlantı kontrolü
echo     ✅ Sipariş yazdırma sistemi
echo     ✅ Detaylı log takibi
echo.
echo  Program başlatılıyor...
echo.

cd /d "%~dp0"

if exist "{exe_name}" (
    echo  ✅ Program dosyası bulundu
    echo  🚀 ÇALIŞAN Fabrika Yazıcı Sistemi başlatılıyor...
    echo.
    
    REM Program başlat
    start "" "{exe_name}"
    
    echo  ✅ Program başlatıldı!
    echo.
    echo  💡 İlk kullanım adımları:
    echo     1. "Yazıcı Yönetimi" sekmesine gidin
    echo     2. "YAZICILARI TARA" butonuna tıklayın
    echo     3. Yazıcınızı seçin ve "YAZICI SEÇ" yapın
    echo     4. "SEÇİLİ YAZICIYI TEST ET" ile test edin
    echo     5. "Ana Kontrol"e geçip "BAĞLANTI TESTİ" yapın
    echo     6. "SİSTEMİ BAŞLAT" butonuna tıklayın
    echo.
    echo  🎯 Artık tüm butonlar gerçekten çalışıyor!
    echo.
    timeout /t 8 >nul
    
) else (
    echo  ❌ HATA: {exe_name} bulunamadı!
    echo.
    echo  Dosyanın bu klasörde olduğundan emin olun.
    echo  Antivirüs programının dosyayı silmediğini kontrol edin.
    echo.
    pause
)
"""
    
    with open(os.path.join(package_dir, "🚀_CALISIR_BASLATMA.bat"), 'w', encoding='utf-8') as f:
        f.write(launcher_content)

def create_test_script(package_dir, exe_name):
    """Test scripti"""
    
    test_content = f"""@echo off
title CALISIR Fabrika Yazici Sistemi - Test Rehberi
cls
color 0E

echo.
echo  ===============================================
echo         🧪 ÇALIŞAN SİSTEM TEST REHBERİ 🧪
echo  ===============================================
echo.
echo  Bu programda TÜM BUTONLAR gerçekten çalışır!
echo.
echo  📋 Test Sırası:
echo.
echo  1️⃣ YAZICI TESTLERI:
echo     • "Yazıcı Yönetimi" sekmesi
echo     • "YAZICILARI TARA" - gerçekten tarar
echo     • "SEÇİLİ YAZICIYI TEST ET" - gerçek yazdırma
echo.
echo  2️⃣ BAĞLANTI TESTLERI:
echo     • "Ana Kontrol" sekmesi  
echo     • "BAĞLANTI TESTİ" - API'yi kontrol eder
echo.
echo  3️⃣ DETAYLI TESTLER:
echo     • "Test Merkezi" sekmesi
echo     • "HIZLI TEST" - anında yazıcı testi
echo     • "METİN TESTİ" - Türkçe karakter testi
echo     • "AĞ TESTİ" - internet bağlantı kontrolü
echo     • "ÖZEL METİN" - kendi metninizi yazdırır
echo.
echo  4️⃣ SİSTEM ÇALIŞTIRMA:
echo     • Yazıcı seçildiğinde "SİSTEMİ BAŞLAT"
echo     • Otomatik sipariş yazdırma başlar
echo.

set /p start="Programı başlatmak istiyor musunuz? (E/H): "

if /i "%start%"=="E" (
    echo.
    echo  🚀 ÇALIŞAN sistem başlatılıyor...
    echo.
    start "" "{exe_name}"
    echo  ✅ Program açıldı! Yukarıdaki test adımlarını takip edin.
    timeout /t 3 >nul
) else (
    echo.
    echo  ❌ Test iptal edildi.
    timeout /t 2 >nul
)
"""
    
    with open(os.path.join(package_dir, "🧪_TEST_REHBERI.bat"), 'w', encoding='utf-8') as f:
        f.write(test_content)

def create_quick_guide(package_dir):
    """Hızlı başlangıç rehberi"""
    
    quick_content = """
⚡ ÇALIŞAN SİSTEM - HIZLI BAŞLANGIÇ
=================================

🎯 3 ADIMDA HAZIR!
==================

1️⃣ PROGRAMI BAŞLAT
-------------------
"🚀_CALISIR_BASLATMA.bat" dosyasına çift tık

2️⃣ YAZICIYI AYARLA  
-------------------
• Yazıcı Yönetimi sekmesi
• "YAZICILARI TARA" (gerçekten tarar!)
• Yazıcıyı seç → "YAZICI SEÇ"
• "SEÇİLİ YAZICIYI TEST ET" (gerçek yazdırma!)

3️⃣ SİSTEMİ ÇALIŞTIR
--------------------
• Ana Kontrol sekmesi
• "BAĞLANTI TESTİ" (API kontrolü!)
• "SİSTEMİ BAŞLAT" → Hazır! ✅

🎉 ARTIK TÜM BUTONLAR ÇALIŞIYOR!

✅ Çalışan Özellikler:
===================
🔄 YAZICILARI TARA - Sistemi gerçekten tarar
🧪 TEST ET - Gerçek test yazdırması yapar
🔍 BAĞLANTI TESTİ - API'yi gerçekten kontrol eder
⚡ HIZLI TEST - Anında yazıcı testi
📄 METİN TESTİ - Türkçe karakter kontrolü
🌐 AĞ TESTİ - İnternet ve API kontrolü
✏️ ÖZEL METİN - Kendi metninizi yazdırır
▶️ SİSTEMİ BAŞLAT - Otomatik sipariş yazdırma

🔧 SORUN VARSA
==============
□ Yazıcı açık mı?
□ USB bağlı mı?
□ İnternet var mı?
□ Windows Defender engelliyor mu?

Bu sürümde hiçbir buton sadece görüntü değil!
Hepsi gerçekten çalışıyor! 🚀
"""
    
    with open(os.path.join(package_dir, "⚡_HIZLI_BASLANGIÇ.txt"), 'w', encoding='utf-8') as f:
        f.write(quick_content)

def create_detailed_guide(package_dir):
    """Detaylı kullanım rehberi"""
    
    detailed_content = """
🏭 ÇALIŞAN FABRİKA YAZICI SİSTEMİ - DETAYLI REHBER
=================================================

🎉 TEBRİKLER!
Bu sürümde TÜM BUTONLAR gerçekten çalışır!
Artık sadece görüntü değil, gerçek işlevsellik var.

📋 SEKMELİ ARAYÜZ REHBERİ
=========================

1️⃣ ANA KONTROL SEKMESİ
----------------------
📊 Sistem Durumu:
• 🖨️ Yazıcı durumu (seçili yazıcı gösterir)
• 🔴/🟢 Bağlantı durumu (gerçek API kontrolü)
• ⏸️/▶️ Servis durumu (çalışıyor/durduruldu)

🎮 Kontrol Paneli:
• ▶️ SİSTEMİ BAŞLAT - Otomatik sipariş dinlemeyi başlatır
• ⏹️ SİSTEMİ DURDUR - Sistemi güvenli şekilde durdurur
• 🔍 BAĞLANTI TESTİ - API bağlantısını gerçekten test eder
• 🔄 YENİLE - Tüm verileri yeniler

📦 Aktif Siparişler:
• Gerçek siparişleri gösterir
• API'den çekilen veriler
• Yazdırma durumları

2️⃣ YAZICI YÖNETİMİ SEKMESİ
---------------------------
🔧 Yazıcı Kontrolleri:
• 🔄 YAZICILARI TARA - Sistemi gerçekten tarar, Windows yazıcılarını bulur
• 🧪 SEÇİLİ YAZICIYI TEST ET - Gerçek test yazdırması yapar
• ✅ YAZICI SEÇ - Seçili yazıcıyı aktif eder

📋 Mevcut Yazıcılar:
• Tüm sistem yazıcıları listelenir
• Durum bilgileri (Hazır/Çevrimdışı/Hata)
• Port ve sürücü bilgileri
• Varsayılan yazıcı işaretlemesi

📌 Seçili Yazıcı:
• Aktif yazıcı bilgisini gösterir

3️⃣ TEST MERKEZİ SEKMESİ
-----------------------
🎯 Test Seçenekleri:
• ⚡ HIZLI TEST - Anında yazıcı bağlantı testi
• 📄 METİN TESTİ - Türkçe karakter ve format testi
• 🖨️ YAZICI DURUMU - Detaylı yazıcı bilgilerini gösterir
• 🌐 AĞ TESTİ - İnternet ve API bağlantı kontrolü

✏️ Özel Test Metni:
• Kendi test metninizi yazabilirsiniz
• 🖨️ ÖZEL METNİ YAZDIR - Yazdığınız metni gerçekten yazdırır

📊 Test Sonuçları:
• Tüm test sonuçları burada görünür
• Gerçek zamanlı sonuç takibi

4️⃣ AYARLAR SEKMESİ
------------------
🔗 API Ayarları:
• API URL (varsayılan: https://siparis.tatopastabaklava.com)
• Güvenlik Token (factory_printer_2024)
• Kontrol Aralığı (30 saniye)

💾 AYARLARI KAYDET:
• Değişiklikleri kalıcı olarak kaydeder

5️⃣ LOGLAR SEKMESİ
-----------------
📝 Sistem Logları:
• Tüm sistem aktiviteleri
• Hata mesajları
• İşlem geçmişi

Kontroller:
• 🔄 LOGLARI YENİLE - Log ekranını günceller
• 🗑️ LOGLARI TEMİZLE - Ekranı temizler
• 💾 DOSYAYA KAYDET - Logları dosyaya kaydeder

🔧 KURULUM VE KULLANIM
======================

📋 İLK KURULUM:
1. Yazıcınızın bilgisayara bağlı ve açık olduğunu kontrol edin
2. "🚀_CALISIR_BASLATMA.bat" dosyasını çalıştırın
3. "Yazıcı Yönetimi" sekmesine gidin
4. "YAZICILARI TARA" butonuna tıklayın (gerçekten tarayacak!)
5. Yazıcınızı listeden seçin
6. "YAZICI SEÇ" butonuna tıklayın
7. "SEÇİLİ YAZICIYI TEST ET" ile test edin (gerçek yazdırma!)

🌐 BAĞLANTI KURULUMU:
1. "Ana Kontrol" sekmesine gidin
2. "BAĞLANTI TESTİ" butonuna tıklayın (gerçek API testi!)
3. Yeşil "Bağlantı: Başarılı" durumunu görmelisiniz
4. API bağlantısı sağlandığında siparişler de yüklenecek

▶️ SİSTEM BAŞLATMA:
1. Yazıcı seçildiğinden ve test edildiğinden emin olun
2. API bağlantısının başarılı olduğunu kontrol edin
3. "SİSTEMİ BAŞLAT" butonuna tıklayın
4. Sistem artık otomatik çalışmaya başlar
5. Yeni siparişler geldiğinde otomatik yazdırılır

🧪 TEST REHBERİ
===============

🔍 YAZICI TESTLERI:
• Önce "YAZICILARI TARA" yapın
• Yazıcınızı seçin
• "SEÇİLİ YAZICIYI TEST ET" ile gerçek test yapın
• Test sayfası yazıcıdan çıkacak

⚡ HIZLI TESTLER:
• "Test Merkezi" sekmesine gidin
• "HIZLI TEST" - anında bağlantı kontrolü
• "METİN TESTİ" - Türkçe karakter testi
• "AĞ TESTİ" - internet ve API kontrolü

✏️ ÖZEL TESTLER:
• Test metin alanına kendi metninizi yazın
• "ÖZEL METNİ YAZDIR" ile gerçek yazdırma
• Sonuçları "Test Sonuçları" alanında takip edin

🔧 SORUN GİDERME
================

🔴 YAZICI BULUNAMIYOR:
□ Yazıcı açık mı?
□ USB kablosu bağlı mı?
□ Windows Ayarlar > Yazıcılar'da görünüyor mu?
□ "YAZICILARI TARA" butonunu tekrar deneyin

🔴 TEST YAZDIRMA ÇALIŞMIYOR:
□ Yazıcıda kağıt var mı?
□ Mürekkep/toner yeterli mi?
□ Yazıcı hazır durumda mı?
□ Başka bir program yazıcıyı kullanıyor mu?

🔴 BAĞLANTI SORUNU:
□ İnternet bağlantınız var mı?
□ "AĞ TESTİ" ile kontrol edin
□ Firewall yazıcı programını engelliyor mu?
□ VPN kullanıyorsanız geçici kapatın

🔴 SİPARİŞLER GELMİYOR:
□ "BAĞLANTI TESTİ" başarılı mı?
□ "SİSTEMİ BAŞLAT" butonuna bastınız mı?
□ Yeşil "Bağlantı: Aktif" durumu görünüyor mu?
□ Token doğru mu? (Ayarlar sekmesi)

💡 İPUÇLARI
============
✅ Programı sürekli açık tutun
✅ Bilgisayarı uyku moduna almayın
✅ Düzenli test yazdırmaları yapın
✅ Log ekranını takip edin
✅ Yazıcı kağıdını kontrol edin

🎯 ÖNEMLİ NOT
=============
Bu sürümde TÜM BUTONLAR gerçekten çalışır!
• YAZICILARI TARA - gerçekten tarar
• TEST ET - gerçek yazdırma yapar
• BAĞLANTI TESTİ - API'yi kontrol eder
• Diğer tüm butonlar da işlevsel

Artık sadece görüntü yok, gerçek işlevsellik var! 🚀

🎉 İYİ KULANIMLAR!
=================
"""
    
    with open(os.path.join(package_dir, "📋_DETAYLI_REHBER.txt"), 'w', encoding='utf-8') as f:
        f.write(detailed_content)

def show_package_contents(package_dir):
    """Paket içeriğini göster"""
    print(f"\n📁 ÇALIŞAN PAKET İÇERİĞİ:")
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
            
            print(f"{icon} {item:<40} {size_str:>10}")
    
    print("=" * 50)
    if total_size > 1024 * 1024:  # MB
        total_size_str = f"{total_size / (1024 * 1024):.1f} MB"
    else:  # KB
        total_size_str = f"{total_size / 1024:.1f} KB"
    
    print(f"📊 Toplam boyut: {total_size_str}")

def main():
    """Ana fonksiyon"""
    if create_working_package():
        print(f"\n🎉 ÇALIŞAN FİNAL PAKET BAŞARIYLA OLUŞTURULDU!")
        
        print("\n📋 Fabrikaya kurulum için:")
        print("1. 'FabrikaYaziciSistemi_CALISIR_FINAL' klasörünü USB'ye kopyalayın")
        print("2. Fabrika bilgisayarında uygun bir yere yapıştırın")
        print("3. '🚀_CALISIR_BASLATMA.bat' dosyasını çalıştırın")
        print("4. Yazıcıyı seçin ve test edin")
        print("5. Sistemi başlatın")
        
        print("\n✅ Bu sürümde TÜM BUTONLAR ÇALIŞIR:")
        print("   🔄 Yazıcı tarama - gerçekten tarar")
        print("   🧪 Test yazdırma - gerçek çıktı verir")
        print("   🔍 Bağlantı testi - API'yi kontrol eder")
        print("   📄 Metin testleri - Türkçe karakter kontrolü")
        print("   🌐 Ağ testleri - internet bağlantı kontrolü")
        print("   ✏️ Özel yazdırma - kendi metninizi yazdırır")
        
        print("\n🎯 Artık sadece görüntü değil, gerçek işlevsellik!")
    else:
        print("\n❌ Çalışan paket oluşturulamadı!")

if __name__ == "__main__":
    main()