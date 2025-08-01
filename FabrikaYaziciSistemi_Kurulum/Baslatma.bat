@echo off
title Fabrika Yazici Sistemi Başlatıcı
cls
color 0A

echo.
echo  ===============================================
echo            TATO PASTA ^& BAKLAVA
echo         FABRİKA YAZICI SİSTEMİ
echo  ===============================================
echo.
echo  📋 Program başlatılıyor...
echo.

REM Geçerli dizini belirle
cd /d "%~dp0"

REM EXE dosyasının varlığını kontrol et
if exist "FabrikaYaziciSistemi.exe" (
    echo  ✅ Program dosyası bulundu
    echo.
    echo  🚀 Yazıcı sistemi başlatılıyor...
    echo.
    
    REM 2 saniye bekle
    timeout /t 2 /nobreak >nul
    
    REM Programı başlat
    start "" "FabrikaYaziciSistemi.exe"
    
    echo  ✅ Program başlatıldı!
    echo.
    echo  📝 Şimdi yapmanız gerekenler:
    echo     1. Bağlantı testini yapın
    echo     2. 'Başlat' butonuna tıklayın
    echo     3. Sistemin siparişleri dinlemesini bekleyin
    echo.
    echo  💡 Bu pencereyi kapatabilirsiniz.
    echo.
    pause
    
) else (
    echo  ❌ HATA: FabrikaYaziciSistemi.exe bulunamadı!
    echo.
    echo  📁 Bu dosyanın bulunduğu klasörde olması gereken dosyalar:
    echo     - FabrikaYaziciSistemi.exe
    echo     - Baslatma.bat (bu dosya)
    echo     - KURULUM_REHBERİ.txt
    echo.
    echo  💡 Dosyaları doğru klasöre kopyaladığınızdan emin olun.
    echo.
    pause
)
