#!/usr/bin/env python3
"""
Fabrika yazıcı programını exe dosyasına dönüştürme scripti
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def create_exe():
    """Fabrika yazıcı programını exe'ye dönüştür"""
    
    print("🔨 Fabrika Yazıcı Programı EXE Oluşturucu")
    print("=" * 50)
    
    # Gerekli dosyaları kontrol et
    main_script = "fabrika_yazici_program.py"
    if not os.path.exists(main_script):
        print(f"❌ {main_script} dosyası bulunamadı!")
        return False
    
    print(f"✅ Ana script bulundu: {main_script}")
    
    # PyInstaller komutunu hazırla
    pyinstaller_cmd = [
        "pyinstaller",
        "--onefile",  # Tek dosya oluştur
        "--windowed",  # Console penceresi gösterme (GUI için)
        "--name=FabrikaYaziciSistemi",  # Exe adı
        "--icon=icon.ico" if os.path.exists("icon.ico") else "",  # İkon varsa ekle
        "--add-data=README_FABRIKA_SISTEMI.md;.",  # Readme dosyasını ekle
        "--hidden-import=tkinter",
        "--hidden-import=tkinter.ttk",
        "--hidden-import=tkinter.scrolledtext",
        "--hidden-import=requests",
        "--hidden-import=json",
        "--hidden-import=threading",
        "--hidden-import=datetime",
        main_script
    ]
    
    # Boş parametreleri temizle
    pyinstaller_cmd = [cmd for cmd in pyinstaller_cmd if cmd]
    
    print("🔧 PyInstaller komutu:")
    print(" ".join(pyinstaller_cmd))
    print()
    
    try:
        # PyInstaller çalıştır
        print("⚙️ EXE oluşturuluyor... (Bu işlem birkaç dakika sürebilir)")
        result = subprocess.run(pyinstaller_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ EXE başarıyla oluşturuldu!")
            
            # Oluşturulan dosyayı kontrol et
            exe_path = "dist/FabrikaYaziciSistemi.exe"
            if os.path.exists(exe_path):
                file_size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
                print(f"📁 EXE dosyası: {exe_path}")
                print(f"📊 Dosya boyutu: {file_size:.1f} MB")
                
                # Fabrika klasörü oluştur ve dosyaları kopyala
                create_factory_package(exe_path)
                
                return True
            else:
                print("❌ EXE dosyası oluşturulamadı!")
                return False
        else:
            print("❌ PyInstaller hatası:")
            print(result.stderr)
            return False
            
    except FileNotFoundError:
        print("❌ PyInstaller bulunamadı! Önce yükleyin: pip install pyinstaller")
        return False
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")
        return False

def create_factory_package(exe_path):
    """Fabrika için kurulum paketi oluştur"""
    
    print("\n📦 Fabrika kurulum paketi oluşturuluyor...")
    
    # Fabrika klasörü oluştur
    package_dir = "FabrikaYaziciSistemi_Kurulum"
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    
    os.makedirs(package_dir)
    
    # EXE dosyasını kopyala
    shutil.copy2(exe_path, package_dir)
    print(f"✅ EXE kopyalandı: {package_dir}/")
    
    # README dosyasını kopyala
    if os.path.exists("README_FABRIKA_SISTEMI.md"):
        shutil.copy2("README_FABRIKA_SISTEMI.md", package_dir)
        print("✅ README kopyalandı")
    
    # Kurulum talimatları oluştur
    create_installation_guide(package_dir)
    
    # Başlatma scripti oluştur
    create_startup_script(package_dir)
    
    print(f"\n🎉 Kurulum paketi hazır: {package_dir}/")
    print("\n📋 Paket içeriği:")
    for file in os.listdir(package_dir):
        file_path = os.path.join(package_dir, file)
        if os.path.isfile(file_path):
            size = os.path.getsize(file_path) / 1024  # KB
            print(f"   📄 {file} ({size:.1f} KB)")

def create_installation_guide(package_dir):
    """Kurulum talimatları oluştur"""
    
    guide_content = """# 🏭 Fabrika Yazıcı Sistemi - Kurulum Rehberi

## 📋 Hızlı Kurulum

### 1. Sistem Gereksinimleri
- Windows 7/8/10/11 (64-bit)
- En az 100 MB boş disk alanı
- İnternet bağlantısı

### 2. Kurulum Adımları

#### Adım 1: Dosyaları Kopyalama
1. Bu klasörü fabrika bilgisayarına kopyalayın
2. Önerilen konum: `C:\\FabrikaYazici\\`

#### Adım 2: Programı Başlatma
1. `FabrikaYaziciSistemi.exe` dosyasına çift tıklayın
2. Windows güvenlik uyarısı çıkarsa "Yine de çalıştır" seçin

#### Adım 3: İlk Ayarlar
1. "🔍 Bağlantı Testi" butonuna tıklayın
2. Bağlantı başarılıysa "▶️ Başlat" butonuna tıklayın
3. Program otomatik olarak siparişleri dinlemeye başlar

### 3. Günlük Kullanım

#### Program Başlatma
- `FabrikaYaziciSistemi.exe` dosyasına çift tıklayın
- Veya `Baslatma.bat` dosyasını kullanın

#### İzleme
- Yeşil "🟢 Bağlı" yazısını görünce sistem hazır
- Yeni siparişler otomatik olarak yazdırılır
- Log alanından işlemleri takip edebilirsiniz

### 4. Sorun Giderme

#### Program Açılmıyor
- Windows Defender'ı geçici olarak kapatın
- Yönetici olarak çalıştırmayı deneyin

#### Bağlantı Sorunu
- İnternet bağlantınızı kontrol edin
- Firewall ayarlarını kontrol edin

#### Yazıcı Sorunu
- Yazıcının açık ve hazır olduğunu kontrol edin
- USB bağlantısını kontrol edin

### 5. Destek
Sorun yaşarsanız:
1. `fabrika_log.txt` dosyasını kontrol edin
2. Log dosyasını sistem yöneticisine gönderin

## 🔧 Gelişmiş Ayarlar

### API Ayarları
- Varsayılan URL: https://siparis.tatopastabaklava.com
- Token: factory_printer_2024
- Kontrol aralığı: 30 saniye

### Log Dosyaları
- Ana log: `fabrika_log.txt`
- Yazdırılan siparişler: `yazdirilanlar/` klasörü

---
🎯 Program hazır! Artık siparişler otomatik yazdırılacak.
"""
    
    with open(os.path.join(package_dir, "KURULUM_REHBERİ.txt"), 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print("✅ Kurulum rehberi oluşturuldu")

def create_startup_script(package_dir):
    """Başlatma scripti oluştur"""
    
    bat_content = """@echo off
title Fabrika Yazici Sistemi
echo.
echo 🏭 Tato Pasta & Baklava - Fabrika Yazici Sistemi
echo ================================================
echo.
echo Program başlatılıyor...
echo.

REM Geçerli dizini al
cd /d "%~dp0"

REM Program varsa başlat
if exist "FabrikaYaziciSistemi.exe" (
    echo ✅ Program bulundu, başlatılıyor...
    start "" "FabrikaYaziciSistemi.exe"
    echo.
    echo ✅ Program başlatıldı!
    echo.
    echo Bu pencereyi kapatabilirsiniz.
    timeout /t 3 >nul
) else (
    echo ❌ FabrikaYaziciSistemi.exe bulunamadı!
    echo.
    echo Bu dosyanın aynı klasörde olduğundan emin olun.
    echo.
    pause
)
"""
    
    with open(os.path.join(package_dir, "Baslatma.bat"), 'w', encoding='utf-8') as f:
        f.write(bat_content)
    
    print("✅ Başlatma scripti oluşturuldu")

def cleanup_build_files():
    """Geçici build dosyalarını temizle"""
    
    print("\n🧹 Geçici dosyalar temizleniyor...")
    
    cleanup_dirs = ["build", "__pycache__"]
    cleanup_files = ["*.spec"]
    
    for dir_name in cleanup_dirs:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✅ Silindi: {dir_name}/")
    
    # .spec dosyalarını sil
    for spec_file in Path(".").glob("*.spec"):
        spec_file.unlink()
        print(f"✅ Silindi: {spec_file}")

def main():
    """Ana fonksiyon"""
    
    print("🚀 EXE oluşturma işlemi başlıyor...\n")
    
    # EXE oluştur
    if create_exe():
        print("\n🎉 İşlem başarıyla tamamlandı!")
        
        # Geçici dosyaları temizle
        cleanup_build_files()
        
        print("\n📦 Fabrika kurulum paketi hazır!")
        print("📁 Klasör: FabrikaYaziciSistemi_Kurulum/")
        print("\n📋 Sonraki adımlar:")
        print("1. 'FabrikaYaziciSistemi_Kurulum' klasörünü fabrika bilgisayarına kopyalayın")
        print("2. 'FabrikaYaziciSistemi.exe' dosyasını çalıştırın")
        print("3. Bağlantı testini yapın ve sistemi başlatın")
        
    else:
        print("\n❌ EXE oluşturma başarısız!")
        return False
    
    return True

if __name__ == "__main__":
    main()