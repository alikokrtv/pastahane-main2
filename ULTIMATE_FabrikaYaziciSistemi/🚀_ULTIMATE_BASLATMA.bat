@echo off
title ULTIMATE Fabrika Yazici Sistemi - Surum Secici
cls
color 0F

echo.
echo  ===============================================
echo         🏭 TATO PASTA ^& BAKLAVA 🏭
echo      ULTIMATE FABRİKA YAZICI SİSTEMİ
echo  ===============================================
echo.
echo  🎯 Hangi sürümü kullanmak istiyorsunuz?
echo.
echo  [1] Temel Sürüm
echo      📋 Hızlı kurulum, basit kullanım
echo.
echo  [2] Gelişmiş Sürüm
echo      📋 Yazıcı yönetimi, test özellikli
echo.
echo  [3] Süper Gelişmiş Sürüm
echo      📋 Otomatik keşif, kapsamlı test
echo.
echo  [0] Çıkış
echo.
echo  💡 Hangi sürümü seçeceğinizi bilmiyorsanız:
echo     - İlk kez kullanıyorsanız → TEMEL
echo     - Yazıcı kontrolü istiyorsanız → GELİŞMİŞ  
echo     - En gelişmiş özellikler → SÜPER GELİŞMİŞ
echo.
set /p choice="Seçiminizi yapın (0-3): "

if "%choice%"=="0" exit

if "%choice%"=="1" (
    echo.
    echo  🚀 Temel Sürüm başlatılıyor...
    echo  📁 Klasör: 1_TEMEL_Hizli_Basit
    cd "1_TEMEL_Hizli_Basit"
    call "Temel_Sürüm_BASLATMA.bat"
    cd ..
    goto end
)

if "%choice%"=="2" (
    echo.
    echo  🚀 Gelişmiş Sürüm başlatılıyor...
    echo  📁 Klasör: 2_GELISMIS_Yazici_Yonetimi
    cd "2_GELISMIS_Yazici_Yonetimi"
    call "Gelişmiş_Sürüm_BASLATMA.bat"
    cd ..
    goto end
)

if "%choice%"=="3" (
    echo.
    echo  🚀 Süper Gelişmiş Sürüm başlatılıyor...
    echo  📁 Klasör: 3_SUPER_Otomatik_Kesfif
    cd "3_SUPER_Otomatik_Kesfif"
    call "Süper_Gelişmiş_Sürüm_BASLATMA.bat"
    cd ..
    goto end
)

echo.
echo  ❌ Geçersiz seçim! Lütfen 0-3 arasında bir sayı girin.
timeout /t 2 >nul
goto start

:start
goto start

:end
echo.
echo  ✅ Program başlatıldı!
pause
