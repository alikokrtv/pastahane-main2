@echo off
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
