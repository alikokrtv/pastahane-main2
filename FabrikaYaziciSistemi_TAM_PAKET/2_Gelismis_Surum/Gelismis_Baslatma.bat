@echo off
title Gelismis Fabrika Yazici Sistemi
cls
color 0B

echo.
echo  ===============================================
echo        GELİŞMİŞ FABRİKA YAZICI SİSTEMİ
echo  ===============================================
echo.
echo  🖨️  Otomatik yazıcı algılama
echo  📊 Detaylı durum takibi
echo  🔧 Gelişmiş ayarlar
echo  📝 Kapsamlı log sistemi
echo.
echo  Program başlatılıyor...
echo.

cd /d "%~dp0"

if exist "GelismisFabrikaYazici.exe" (
    start "" "GelismisFabrikaYazici.exe"
    echo  ✅ Gelişmiş sürüm başlatıldı!
    timeout /t 3 >nul
) else (
    echo  ❌ EXE dosyası bulunamadı!
    pause
)
