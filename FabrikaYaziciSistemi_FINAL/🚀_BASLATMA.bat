@echo off
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

if exist "FabrikaYaziciSistemi.exe" (
    echo  ✅ Program dosyası bulundu
    echo  🚀 Fabrika Yazıcı Sistemi başlatılıyor...
    echo.
    
    REM Program başlat
    start "" "FabrikaYaziciSistemi.exe"
    
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
    echo  ❌ HATA: FabrikaYaziciSistemi.exe bulunamadı!
    echo.
    echo  Dosyanın bu klasörde olduğundan emin olun.
    echo  Antivirüs programının dosyayı silmediğini kontrol edin.
    echo.
    pause
)
