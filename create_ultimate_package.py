#!/usr/bin/env python3
"""
Ultimate Fabrika Yazıcı Sistemi - 3 Sürüm Bir Arada
Temel, Gelişmiş ve Süper Gelişmiş sürümleri içeren tam paket
"""

import os
import shutil
from pathlib import Path

def create_ultimate_package():
    """Ultimate kurulum paketi oluştur"""
    
    print("🚀 ULTIMATE FABRİKA YAZICI SİSTEMİ PAKETİ")
    print("=" * 70)
    
    # EXE dosyalarını kontrol et
    exe_files = {
        'basic': 'dist/FabrikaYaziciSistemi.exe',
        'advanced': 'dist/GelismisFabrikaYazici.exe', 
        'super': 'dist/SuperGelismisFabrikaYazici.exe'
    }
    
    available_versions = {}
    
    print("📋 Mevcut Sürümler:")
    for version, path in exe_files.items():
        if os.path.exists(path):
            size = os.path.getsize(path) / (1024 * 1024)  # MB
            print(f"   ✅ {version.upper()}: {path} ({size:.1f} MB)")
            available_versions[version] = path
        else:
            print(f"   ❌ {version.upper()}: {path} - BULUNAMADI")
    
    if not available_versions:
        print("❌ Hiçbir EXE dosyası bulunamadı!")
        return False
    
    # Ana kurulum klasörü oluştur
    package_dir = "ULTIMATE_FabrikaYaziciSistemi"
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
        print(f"🗑️ Eski paket temizlendi")
    
    os.makedirs(package_dir)
    print(f"📁 Ultimate paket klasörü oluşturuldu: {package_dir}")
    
    # Sürüm klasörlerini oluştur
    version_info = {
        'basic': {
            'dir': '1_TEMEL_Hizli_Basit',
            'name': 'Temel Sürüm',
            'desc': 'Hızlı kurulum, basit kullanım'
        },
        'advanced': {
            'dir': '2_GELISMIS_Yazici_Yonetimi', 
            'name': 'Gelişmiş Sürüm',
            'desc': 'Yazıcı yönetimi, test özellikli'
        },
        'super': {
            'dir': '3_SUPER_Otomatik_Kesfif',
            'name': 'Süper Gelişmiş Sürüm', 
            'desc': 'Otomatik keşif, kapsamlı test'
        }
    }
    
    created_versions = []
    
    # Her sürümü hazırla
    for version, exe_path in available_versions.items():
        if version in version_info:
            version_dir = os.path.join(package_dir, version_info[version]['dir'])
            os.makedirs(version_dir)
            
            create_version_package(version_dir, exe_path, version, version_info[version])
            created_versions.append(version)
            print(f"✅ {version_info[version]['name']} hazırlandı")
    
    # Ortak dosyalar klasörü
    common_dir = os.path.join(package_dir, "4_ORTAK_Dokumantasyon")
    os.makedirs(common_dir)
    create_common_files(common_dir)
    print("✅ Ortak dosyalar hazırlandı")
    
    # Ana başlatma dosyaları
    create_main_launcher(package_dir, created_versions, version_info)
    create_ultimate_readme(package_dir, created_versions, version_info)
    create_quick_start_guide(package_dir)
    
    # Paket içeriğini göster
    show_ultimate_package_contents(package_dir)
    
    print(f"\n🎉 ULTIMATE KURULUM PAKETİ HAZIR!")
    print(f"📂 Konum: {os.path.abspath(package_dir)}")
    print(f"🔢 İçerik: {len(created_versions)} farklı sürüm + dokümantasyon")
    
    return True

def create_version_package(version_dir, exe_path, version_type, version_info):
    """Belirli bir sürüm paketi oluştur"""
    
    # EXE dosyasını kopyala
    exe_name = os.path.basename(exe_path)
    shutil.copy2(exe_path, version_dir)
    
    # Sürüme özel başlatma scripti
    launcher_content = create_version_launcher(version_type, version_info, exe_name)
    
    launcher_name = f"{version_info['name'].replace(' ', '_')}_BASLATMA.bat"
    with open(os.path.join(version_dir, launcher_name), 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    
    # Sürüme özel README
    readme_content = create_version_readme(version_type, version_info)
    
    readme_name = f"{version_info['name'].replace(' ', '_')}_REHBERI.txt"
    with open(os.path.join(version_dir, readme_name), 'w', encoding='utf-8') as f:
        f.write(readme_content)

def create_version_launcher(version_type, version_info, exe_name):
    """Sürüme özel başlatma scripti"""
    
    colors = {
        'basic': '0A',      # Yeşil
        'advanced': '0B',   # Turkuaz 
        'super': '0D'       # Mor
    }
    
    icons = {
        'basic': '⚡',
        'advanced': '🔧', 
        'super': '🚀'
    }
    
    color = colors.get(version_type, '0F')
    icon = icons.get(version_type, '📱')
    
    return f"""@echo off
title {version_info['name']} - Fabrika Yazici Sistemi
cls
color {color}

echo.
echo  ===============================================
echo         {icon} {version_info['name'].upper()} {icon}
echo         TATO PASTA ^& BAKLAVA
echo  ===============================================
echo.
echo  📋 Özellikler: {version_info['desc']}
echo.
echo  Program başlatılıyor...
echo.

cd /d "%~dp0"

if exist "{exe_name}" (
    echo  ✅ Program dosyası bulundu
    echo  🚀 {version_info['name']} başlatılıyor...
    echo.
    start "" "{exe_name}"
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
    echo  ❌ HATA: {exe_name} bulunamadı!
    echo.
    echo  Dosyanın bu klasörde olduğundan emin olun.
    echo.
    pause
)
"""

def create_version_readme(version_type, version_info):
    """Sürüme özel README"""
    
    features = {
        'basic': [
            "✅ Basit ve kullanıcı dostu arayüz",
            "✅ Otomatik sipariş dinleme",
            "✅ Hızlı yazdırma",
            "✅ Temel log sistemi",
            "✅ API bağlantı kontrolü",
            "❌ Yazıcı yönetimi yok",
            "❌ Gelişmiş test yok"
        ],
        'advanced': [
            "✅ Sekmeli gelişmiş arayüz",
            "✅ Yazıcı yönetimi",
            "✅ Test yazdırma",
            "✅ Detaylı log sistemi", 
            "✅ Gelişmiş ayarlar",
            "✅ Yazıcı durum kontrolü",
            "❌ Otomatik keşif yok"
        ],
        'super': [
            "✅ Otomatik yazıcı keşfi",
            "✅ Ağ yazıcıları bulma",
            "✅ Kapsamlı test merkezi",
            "✅ Yazıcı yetenekleri analizi",
            "✅ Kurulum sihirbazı",
            "✅ Canlı durum takibi",
            "✅ 6 sekmeli süper arayüz"
        ]
    }
    
    recommendations = {
        'basic': [
            "👥 İlk kez kullananlar",
            "⚡ Hızlı kurulum isteyenler",
            "🎯 Basit ihtiyaçları olanlar",
            "💻 Tek yazıcısı olanlar"
        ],
        'advanced': [
            "🔧 Yazıcı kontrolü isteyenler",
            "🧪 Test yazdırma ihtiyacı olanlar",
            "📊 Detaylı log isteyenler",
            "⚙️ Gelişmiş ayarlar isteyenler"
        ],
        'super': [
            "🖨️ Birden fazla yazıcısı olanlar",
            "🌐 Ağ yazıcıları olanlar",
            "🧪 Kapsamlı test isteyenler",
            "🚀 En gelişmiş özellikleri isteyenler"
        ]
    }
    
    content = f"""
🏭 {version_info['name'].upper()}
{version_info['desc']}
{'=' * 50}

✨ ÖZELLIKLER
{'=' * 15}
"""
    
    for feature in features.get(version_type, []):
        content += f"{feature}\n"
    
    content += f"""
👥 KİMLER KULLANMALI
{'=' * 20}
"""
    
    for rec in recommendations.get(version_type, []):
        content += f"{rec}\n"
    
    content += f"""
🚀 HIZLI BAŞLANGIÇ
{'=' * 18}
1. "{version_info['name'].replace(' ', '_')}_BASLATMA.bat" dosyasına çift tıklayın
2. Program otomatik olarak açılır
3. İlk kurulum adımlarını takip edin
4. Sistem çalışmaya başlar

🔧 SİSTEM GEREKSİNİMLERİ
{'=' * 25}
- Windows 7/8/10/11 (64-bit)
- En az 50 MB boş alan
- İnternet bağlantısı
- USB veya ağ yazıcısı

💡 İPUÇLARI
{'=' * 12}
- İlk kurulumda mutlaka bağlantı testi yapın
- Yazıcınızın açık olduğundan emin olun
- Sorun yaşarsanız log dosyalarını kontrol edin

📞 YARDIM
{'=' * 9}
Sorun yaşarsanız "4_ORTAK_Dokumantasyon" klasöründeki
rehberleri okuyun veya sistem yöneticisiyle iletişime geçin.

🎉 İYİ KULANIMLAR!
"""
    
    return content

def create_common_files(common_dir):
    """Ortak dosyalar oluştur"""
    
    # Ana dokümantasyon dosyalarını kopyala
    docs_to_copy = [
        "README_FABRIKA_SISTEMI.md",
        "KURULUM_TAMAMLANDI.md"
    ]
    
    for doc in docs_to_copy:
        if os.path.exists(doc):
            shutil.copy2(doc, common_dir)
    
    # Sistem karşılaştırma tablosu
    comparison_content = """
🔍 SÜRÜM KARŞILAŞTIRMA TABLOSU
==============================

                          TEMEL    GELİŞMİŞ    SÜPER
                          -----    --------    -----
Arayüz                      ⭐       ⭐⭐⭐       ⭐⭐⭐⭐⭐
Kullanım Kolaylığı        ⭐⭐⭐⭐⭐    ⭐⭐⭐⭐      ⭐⭐⭐
Yazıcı Yönetimi             ❌       ✅         ✅
Otomatik Keşif              ❌       ❌         ✅
Test Özellikleri            ❌       ⭐⭐        ⭐⭐⭐⭐⭐
Ağ Yazıcı Desteği           ❌       ⭐         ⭐⭐⭐⭐⭐
Log Sistemi               ⭐⭐       ⭐⭐⭐       ⭐⭐⭐⭐⭐
Ayar Seçenekleri          ⭐⭐       ⭐⭐⭐⭐      ⭐⭐⭐⭐⭐
Sorun Giderme             ⭐⭐       ⭐⭐⭐       ⭐⭐⭐⭐⭐

🎯 DOĞRU SEÇİM REHBERİ
======================

🔹 TEMEL SÜRÜM SEÇİN EĞER:
- İlk kez kullanıyorsanız
- Tek bir USB yazıcınız varsa  
- Basit ihtiyaçlarınız varsa
- Hızlı kurulum istiyorsanız

🔹 GELİŞMİŞ SÜRÜM SEÇİN EĞER:
- Yazıcı kontrolü istiyorsanız
- Test yazdırma ihtiyacınız varsa
- Detaylı ayarlar istiyorsanız
- Orta seviye kullanıcıysanız

🔹 SÜPER GELİŞMİŞ SÜRÜM SEÇİN EĞER:
- Birden fazla yazıcınız varsa
- Ağ yazıcıları kullanıyorsanız
- En gelişmiş özellikleri istiyorsanız
- Teknik bilginiz iyiyse

💡 KARARSIZ KALIYORSANIZ:
GELİŞMİŞ SÜRÜM ile başlayın, gerekirse
SÜPER GELİŞMİŞ'e geçebilirsiniz.
"""
    
    with open(os.path.join(common_dir, "SURUM_KARSILASTIRMA.txt"), 'w', encoding='utf-8') as f:
        f.write(comparison_content)
    
    # Sorun giderme rehberi
    troubleshooting_content = """
🔧 ULTIMATE SORUN GİDERME REHBERİ
=================================

🔴 PROGRAM AÇILMIYOR
-------------------
□ Windows Defender'ı geçici olarak kapatın
□ Dosyaya sağ tık → "Yönetici olarak çalıştır"
□ Antivirüs programının engellemediğini kontrol edin
□ .NET Framework güncel olduğundan emin olun

🔴 YAZICI BULUNAMIYOR  
--------------------
□ Yazıcının açık ve hazır olduğunu kontrol edin
□ USB kablosunu çıkarıp takın
□ Yazıcı sürücülerinin yüklendiğini kontrol edin
□ Windows Yazıcılar ayarlarından yazıcıyı görebildiğinizi kontrol edin
□ SÜPER GELİŞMİŞ sürümde "Yazıcı Keşfi" özelliğini kullanın

🔴 API BAĞLANTI SORUNU
---------------------
□ İnternet bağlantınızı test edin (web sitesi açın)
□ Firewall'un programı engellemediğini kontrol edin
□ Şirket ağındaysanız IT departmanıyla konuşun
□ VPN kullanıyorsanız geçici olarak kapatın
□ Token'ın doğru olduğunu kontrol edin

🔴 YAZDIRMA ÇALIŞMIYOR
---------------------
□ Test yazdırma özelliğini kullanın
□ Yazıcı kuyruğunu kontrol edin
□ Kağıt ve mürekkep/toner durumunu kontrol edin  
□ Yazıcıyı yeniden başlatın
□ Windows yazıcı sorun gidericisini çalıştırın

🔴 PROGRAM YAVAŞ ÇALIŞIYOR
-------------------------
□ İnternet hızınızı test edin
□ Kontrol aralığını artırın (Ayarlar)
□ Gereksiz programları kapatın
□ Bilgisayarı yeniden başlatın

🔴 SİPARİŞLER GELMİYOR
---------------------
□ "Başlat" butonuna bastığınızı kontrol edin
□ Yeşil "Bağlı" durumunu kontrol edin
□ Manuel "Yenile" butonunu deneyin
□ API token'ının doğru olduğunu kontrol edin
□ Sistem yöneticisiyle iletişime geçin

📞 ACİL YARDIM PROTOKOLÜ
=======================
1. Log dosyasını açın (fabrika_log.txt)
2. En son hata mesajlarını kopyalayın
3. Hangi sürümü kullandığınızı belirtin
4. Sistem yöneticisine iletin
5. Varsa ekran görüntüsü alın

🏆 PERFORMANS İPUÇLARI
=====================
□ Programı sürekli açık tutun
□ Bilgisayarı uyku moduna almayın
□ Düzenli olarak log dosyalarını temizleyin
□ Yazıcı kağıdını kontrol edin
□ İnternet bağlantısını stabil tutun

Bu rehber tüm sürümler için geçerlidir.
Daha detaylı yardım için ilgili sürümün
kendi rehberini okuyun.
"""
    
    with open(os.path.join(common_dir, "SORUN_GIDERME_ULTIMATE.txt"), 'w', encoding='utf-8') as f:
        f.write(troubleshooting_content)

def create_main_launcher(package_dir, created_versions, version_info):
    """Ana başlatma dosyası"""
    
    launcher_content = """@echo off
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
"""
    
    option_num = 1
    for version in created_versions:
        if version in version_info:
            info = version_info[version]
            launcher_content += f"""echo  [{option_num}] {info['name']}
echo      📋 {info['desc']}
echo.
"""
            option_num += 1
    
    launcher_content += """echo  [0] Çıkış
echo.
echo  💡 Hangi sürümü seçeceğinizi bilmiyorsanız:
echo     - İlk kez kullanıyorsanız → TEMEL
echo     - Yazıcı kontrolü istiyorsanız → GELİŞMİŞ  
echo     - En gelişmiş özellikler → SÜPER GELİŞMİŞ
echo.
set /p choice="Seçiminizi yapın (0-3): "

if "%choice%"=="0" exit
"""
    
    option_num = 1
    for version in created_versions:
        if version in version_info:
            info = version_info[version]
            dir_name = info['dir']
            launcher_name = f"{info['name'].replace(' ', '_')}_BASLATMA.bat"
            
            launcher_content += f"""
if "%choice%"=="{option_num}" (
    echo.
    echo  🚀 {info['name']} başlatılıyor...
    echo  📁 Klasör: {dir_name}
    cd "{dir_name}"
    call "{launcher_name}"
    cd ..
    goto end
)
"""
            option_num += 1
    
    launcher_content += """
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
"""
    
    with open(os.path.join(package_dir, "🚀_ULTIMATE_BASLATMA.bat"), 'w', encoding='utf-8') as f:
        f.write(launcher_content)

def create_ultimate_readme(package_dir, created_versions, version_info):
    """Ultimate README dosyası"""
    
    readme_content = f"""
🏭 ULTIMATE FABRİKA YAZICI SİSTEMİ PAKETİ
========================================

🎉 TEBRİKLER! 
Bu pakette {len(created_versions)} farklı sürüm bulunmaktadır.
İhtiyacınıza en uygun olanı seçebilirsiniz.

🚀 HIZLI BAŞLANGIÇ
=================
1. "🚀_ULTIMATE_BASLATMA.bat" dosyasına çift tıklayın
2. İhtiyacınıza uygun sürümü seçin
3. Program otomatik olarak başlar
4. İlk kurulum adımlarını takip edin

📁 PAKET İÇERİĞİ
===============
"""
    
    for version in created_versions:
        if version in version_info:
            info = version_info[version]
            readme_content += f"""
📂 {info['dir']}/
   🔧 Program dosyası ({info['name']})
   ⚡ Başlatma scripti
   📄 Kullanım rehberi
"""
    
    readme_content += """
📂 4_ORTAK_Dokumantasyon/
   📋 Sürüm karşılaştırma tablosu
   🔧 Sorun giderme rehberi
   📄 Teknik dokümantasyon

⚡ 🚀_ULTIMATE_BASLATMA.bat - Ana başlatma dosyası
📄 ULTIMATE_REHBER.txt - Bu dosya
📄 HIZLI_BASLANGIÇ.txt - Hızlı kurulum rehberi

🎯 SÜRÜM SEÇİM REHBERİ
=====================
"""
    
    selection_guide = {
        'basic': "👶 Yeni başlayanlar, basit kullanım",
        'advanced': "🔧 Orta seviye, yazıcı kontrolü", 
        'super': "🚀 İleri seviye, tüm özellikler"
    }
    
    for version in created_versions:
        if version in version_info and version in selection_guide:
            info = version_info[version]
            readme_content += f"\n🔹 {info['name']}: {selection_guide[version]}"
    
    readme_content += """

💡 KARARSIZ KALIYORSANIZ
=======================
"GELİŞMİŞ SÜRÜM" ile başlamanızı öneririz.
Hem kolay kullanım hem de yeterli özellik sunar.

🔧 SİSTEM GEREKSİNİMLERİ
=======================
- Windows 7/8/10/11 (64-bit önerilen)
- En az 100 MB boş disk alanı
- İnternet bağlantısı (sürekli)
- USB veya ağ yazıcısı

📞 DESTEK
=========
Sorun yaşarsanız:
1. İlgili sürümün kendi rehberini okuyun
2. "4_ORTAK_Dokumantasyon" klasöründeki
   sorun giderme rehberini kontrol edin
3. Sistem yöneticisiyle iletişime geçin

🎉 SİSTEM HAZIR!
===============
Artık şubelerden gelen siparişler
fabrikada otomatik yazdırılacak!

İyi kullanımlar! 🎯
"""
    
    with open(os.path.join(package_dir, "ULTIMATE_REHBER.txt"), 'w', encoding='utf-8') as f:
        f.write(readme_content)

def create_quick_start_guide(package_dir):
    """Hızlı başlangıç rehberi"""
    
    quick_content = """
⚡ SÜPER HIZLI BAŞLANGIÇ REHBERİ
==============================

🎯 3 ADIMDA BAŞLAYIN
===================

1️⃣ ANA BAŞLATMA
--------------
"🚀_ULTIMATE_BASLATMA.bat" dosyasına çift tıklayın

2️⃣ SÜRÜM SEÇİMİ  
---------------
Kararsızsanız: "2" (Gelişmiş Sürüm) seçin

3️⃣ İLK KURULUM
--------------
Program açıldığında:
✅ Yazıcıyı seçin/kontrol edin
✅ "Bağlantı Testi" yapın  
✅ "Başlat" butonuna tıklayın

🎉 HAZIR! Artık siparişler otomatik yazdırılıyor!

🔧 SORUN YAŞIYORSANIZ
====================
□ Windows Defender'ı geçici kapatın
□ Yazıcının açık olduğunu kontrol edin
□ İnternet bağlantısını test edin

📞 Yardım: "4_ORTAK_Dokumantasyon" klasörü

Bu kadar basit! 🚀
"""
    
    with open(os.path.join(package_dir, "⚡_HIZLI_BASLANGIÇ.txt"), 'w', encoding='utf-8') as f:
        f.write(quick_content)

def show_ultimate_package_contents(package_dir):
    """Ultimate paket içeriğini göster"""
    print(f"\n📁 ULTIMATE PAKET İÇERİĞİ:")
    print("=" * 60)
    
    total_size = 0
    
    def show_directory(dir_path, indent=""):
        nonlocal total_size
        
        if not os.path.exists(dir_path):
            return
        
        for item in sorted(os.listdir(dir_path)):
            item_path = os.path.join(dir_path, item)
            
            if os.path.isfile(item_path):
                size = os.path.getsize(item_path)
                total_size += size
                
                if size > 1024 * 1024:  # MB
                    size_str = f"{size / (1024 * 1024):.1f} MB"
                elif size > 1024:  # KB
                    size_str = f"{size / 1024:.1f} KB"
                else:
                    size_str = f"{size} bytes"
                
                # Dosya türüne göre ikon
                if item.endswith('.exe'):
                    icon = "🔧"
                elif item.endswith('.bat'):
                    icon = "⚡"
                elif item.endswith('.txt'):
                    icon = "📄"
                elif item.endswith('.md'):
                    icon = "📋"
                else:
                    icon = "📁"
                
                print(f"{indent}{icon} {item:<40} {size_str:>10}")
            
            elif os.path.isdir(item_path):
                print(f"{indent}📂 {item}/")
                show_directory(item_path, indent + "   ")
    
    show_directory(package_dir)
    
    print("=" * 60)
    if total_size > 1024 * 1024:  # MB
        total_size_str = f"{total_size / (1024 * 1024):.1f} MB"
    else:  # KB
        total_size_str = f"{total_size / 1024:.1f} KB"
    
    print(f"📊 Toplam boyut: {total_size_str}")

def main():
    """Ana fonksiyon"""
    if create_ultimate_package():
        print(f"\n🎉 ULTIMATE PAKET BAŞARIYLA OLUŞTURULDU!")
        
        print("\n📋 Fabrikaya kurulum için:")
        print("1. 'ULTIMATE_FabrikaYaziciSistemi' klasörünü USB'ye kopyalayın")
        print("2. Fabrika bilgisayarında uygun bir yere yapıştırın")
        print("3. '🚀_ULTIMATE_BASLATMA.bat' dosyasını çalıştırın")
        print("4. İhtiyacınıza göre sürüm seçin")
        print("5. İlk kurulum adımlarını takip edin")
        
        print("\n💡 Sürüm önerileri:")
        print("   ⚡ İlk kez kullanım: TEMEL SÜRÜM")
        print("   🔧 Orta seviye: GELİŞMİŞ SÜRÜM") 
        print("   🚀 İleri seviye: SÜPER GELİŞMİŞ SÜRÜM")
    else:
        print("\n❌ Ultimate paket oluşturulamadı!")

if __name__ == "__main__":
    main()