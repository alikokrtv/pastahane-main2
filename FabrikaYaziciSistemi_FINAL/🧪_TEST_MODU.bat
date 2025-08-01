@echo off
title Fabrika Yazici Sistemi - Test Modu
cls
color 0E

echo.
echo  ===============================================
echo         🧪 TEST MODU BAŞLATILIYOR 🧪
echo       FABRİKA YAZICI SİSTEMİ
echo  ===============================================
echo.
echo  Bu mod sadece test amaçlıdır.
echo  Gerçek siparişler yazdırılmayacak.
echo.
echo  Test özellikları:
echo     🔍 Yazıcı bağlantı testi
echo     🖨️ Test yazdırma
echo     🌐 API bağlantı kontrolü
echo     📊 Sistem durum raporu
echo.

set /p confirm="Test modunu başlatmak istiyor musunuz? (E/H): "

if /i "%confirm%"=="E" (
    echo.
    echo  🚀 Test modu başlatılıyor...
    echo.
    start "" "FabrikaYaziciSistemi.exe"
    echo  ✅ Test modu aktif!
    echo  💡 Program açıldığında "Test Merkezi" sekmesini kullanın.
    timeout /t 3 >nul
) else (
    echo.
    echo  ❌ Test modu iptal edildi.
    timeout /t 2 >nul
)
