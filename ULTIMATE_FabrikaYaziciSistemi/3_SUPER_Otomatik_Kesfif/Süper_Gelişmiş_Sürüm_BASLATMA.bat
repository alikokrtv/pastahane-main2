@echo off
title Süper Gelişmiş Sürüm - Fabrika Yazici Sistemi
cls
color 0D

echo.
echo  ===============================================
echo         🚀 SÜPER GELIŞMIŞ SÜRÜM 🚀
echo         TATO PASTA ^& BAKLAVA
echo  ===============================================
echo.
echo  📋 Özellikler: Otomatik keşif, kapsamlı test
echo.
echo  Program başlatılıyor...
echo.

cd /d "%~dp0"

if exist "SuperGelismisFabrikaYazici.exe" (
    echo  ✅ Program dosyası bulundu
    echo  🚀 Süper Gelişmiş Sürüm başlatılıyor...
    echo.
    start "" "SuperGelismisFabrikaYazici.exe"
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
    echo  ❌ HATA: SuperGelismisFabrikaYazici.exe bulunamadı!
    echo.
    echo  Dosyanın bu klasörde olduğundan emin olun.
    echo.
    pause
)
