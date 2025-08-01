@echo off
title Gelişmiş Sürüm - Fabrika Yazici Sistemi
cls
color 0B

echo.
echo  ===============================================
echo         🔧 GELIŞMIŞ SÜRÜM 🔧
echo         TATO PASTA ^& BAKLAVA
echo  ===============================================
echo.
echo  📋 Özellikler: Yazıcı yönetimi, test özellikli
echo.
echo  Program başlatılıyor...
echo.

cd /d "%~dp0"

if exist "GelismisFabrikaYazici.exe" (
    echo  ✅ Program dosyası bulundu
    echo  🚀 Gelişmiş Sürüm başlatılıyor...
    echo.
    start "" "GelismisFabrikaYazici.exe"
    echo  ✅ Program başlatıldı!
    echo.
    echo  💡 Şimdi yapmanız gerekenler:
    echo     1. Yazıcı bağlantısını kontrol edin
    echo     2. API bağlantı testini yapın
    echo     3. Sistemi başlatın
    echo.
    echo  Bu pencereyi kapatabilirsiniz.
    timeout /t 5 >nul
) else (
    echo  ❌ HATA: GelismisFabrikaYazici.exe bulunamadı!
    echo.
    echo  Dosyanın bu klasörde olduğundan emin olun.
    echo.
    pause
)
