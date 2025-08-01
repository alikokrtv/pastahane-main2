@echo off
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

if exist "FabrikaYaziciSistemi.exe" (
    echo  ✅ Program dosyası bulundu
    echo  🚀 ÇALIŞAN Fabrika Yazıcı Sistemi başlatılıyor...
    echo.
    
    REM Program başlat
    start "" "FabrikaYaziciSistemi.exe"
    
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
    echo  ❌ HATA: FabrikaYaziciSistemi.exe bulunamadı!
    echo.
    echo  Dosyanın bu klasörde olduğundan emin olun.
    echo  Antivirüs programının dosyayı silmediğini kontrol edin.
    echo.
    pause
)
