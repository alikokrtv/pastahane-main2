@echo off
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
    start "" "FabrikaYaziciSistemi.exe"
    echo  ✅ Program açıldı! Yukarıdaki test adımlarını takip edin.
    timeout /t 3 >nul
) else (
    echo.
    echo  ❌ Test iptal edildi.
    timeout /t 2 >nul
)
