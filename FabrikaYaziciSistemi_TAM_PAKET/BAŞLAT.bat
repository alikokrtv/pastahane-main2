@echo off
title Fabrika Yazici Sistemi - Surum Secici
cls
color 0F

echo.
echo  ===============================================
echo           TATO PASTA ^& BAKLAVA
echo         FABRİKA YAZICI SİSTEMİ
echo  ===============================================
echo.
echo  Hangi sürümü kullanmak istiyorsunuz?
echo.
echo  [1] Temel Sürüm - Basit ve hızlı kullanım
echo      ✅ Kolay kullanım
echo      ✅ Temel özellikler
echo.
echo  [2] Gelişmiş Sürüm - Detaylı kontrol
echo      ✅ Otomatik yazıcı algılama
echo      ✅ Gelişmiş özellikler
echo      ✅ Detaylı ayarlar
echo.
echo  [0] Çıkış
echo.
:start
set /p choice="Seçiminizi yapın: "

if "%choice%"=="0" exit

if "%choice%"=="1" (
    echo.
    echo  🚀 Temel sürüm başlatılıyor...
    cd "1_Temel_Surum"
    call "Temel_Baslatma.bat"
    cd ..
    goto end
)

if "%choice%"=="2" (
    echo.
    echo  🚀 Gelişmiş sürüm başlatılıyor...
    cd "2_Gelismis_Surum"
    call "Gelismis_Baslatma.bat"
    cd ..
    goto end
)

echo.
echo  ❌ Geçersiz seçim! Lütfen tekrar deneyin.
timeout /t 2 >nul
goto start

:end
echo.
echo  ✅ Program başlatıldı!
pause
