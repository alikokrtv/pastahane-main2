@echo off
title Yazıcı Test Programı
cls
color 0B

echo.
echo  ===============================================
echo            YAZICI TEST PROGRAMI
echo  ===============================================
echo.
echo  🖨️  Yazıcı bağlantısı test ediliyor...
echo.

REM Test metni oluştur
echo Test yazdırma - %date% %time% > test_ciktisi.txt
echo. >> test_ciktisi.txt
echo TATO PASTA ^& BAKLAVA >> test_ciktisi.txt
echo Fabrika Yazıcı Sistemi >> test_ciktisi.txt
echo. >> test_ciktisi.txt
echo Bu bir test çıktısıdır. >> test_ciktisi.txt
echo Eğer bu metni görebiliyorsanız >> test_ciktisi.txt
echo yazıcınız çalışıyor demektir. >> test_ciktisi.txt
echo. >> test_ciktisi.txt
echo Test tarihi: %date% >> test_ciktisi.txt
echo Test saati: %time% >> test_ciktisi.txt

REM Varsayılan yazıcıya gönder
echo  📄 Test dosyası oluşturuldu: test_ciktisi.txt
echo.
echo  🖨️  Varsayılan yazıcıya gönderiliyor...

print test_ciktisi.txt

echo.
echo  ✅ Test tamamlandı!
echo.
echo  📋 Sonuç:
echo     - Yazıcıdan çıktı aldıysanız: Yazıcı hazır ✅
echo     - Çıktı alamadıysanız: Yazıcı ayarlarını kontrol edin ❌
echo.
echo  💡 Sorun yaşıyorsanız:
echo     1. Yazıcının açık olduğunu kontrol edin
echo     2. USB bağlantısını kontrol edin  
echo     3. Windows yazıcı ayarlarını kontrol edin
echo.
pause
