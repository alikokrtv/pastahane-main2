@echo off
title Temel Sürüm - Fabrika Yazici Sistemi
cls
color 0A

echo.
echo  ===============================================
echo         ⚡ TEMEL SÜRÜM ⚡
echo         TATO PASTA ^& BAKLAVA
echo  ===============================================
echo.
echo  📋 Özellikler: Hızlı kurulum, basit kullanım
echo.
echo  Program başlatılıyor...
echo.

cd /d "%~dp0"

if exist "FabrikaYaziciSistemi.exe" (
    echo  ✅ Program dosyası bulundu
    echo  🚀 Temel Sürüm başlatılıyor...
    echo.
    start "" "FabrikaYaziciSistemi.exe"
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
    echo  ❌ HATA: FabrikaYaziciSistemi.exe bulunamadı!
    echo.
    echo  Dosyanın bu klasörde olduğundan emin olun.
    echo.
    pause
)
