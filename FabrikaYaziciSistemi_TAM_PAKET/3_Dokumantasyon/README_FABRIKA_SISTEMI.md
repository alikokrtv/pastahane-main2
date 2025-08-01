# 🏭 Tato Pasta & Baklava - Fabrika Yazıcı Sistemi

## 📋 Sistem Özeti

Bu sistem, Coolify'da çalışan pastane yönetim sistemini dinleyerek fabrikaya gelen yeni siparişleri otomatik olarak yazıcıdan çıkaran bir uygulamadır.

## 🎯 Özellikler

### ✅ Tamamlanan Görevler
1. **Excel Ürün Aktarımı**: YENİ PASTA LİSTE YAZILIM.xlsx dosyasındaki ürünler sisteme aktarıldı
2. **Şube Müdürleri**: Vega ve Çarşı şube müdürleri oluşturuldu
3. **Fabrika API'leri**: Yeni sipariş dinleme ve yazdırma API'leri eklendi
4. **Yazıcı Programı**: Uzaktan çalışacak GUI yazıcı programı geliştirildi

### 🔑 Giriş Bilgileri

#### Şube Müdürleri
- **Vega Şube Müdürü**: 
  - Kullanıcı adı: `vega_mudur`
  - Şifre: `vega123`
  - URL: https://siparis.tatopastabaklava.com

- **Çarşı Şube Müdürü**: 
  - Kullanıcı adı: `carsi_mudur`
  - Şifre: `carsi123`
  - URL: https://siparis.tatopastabaklava.com

## 🖥️ Sistem Bileşenleri

### 1. Şube Sipariş Arayüzü
- Şube müdürleri web arayüzünden günlük sipariş oluşturabilir
- Excel'deki ürün listesinden seçim yapabilir
- Yarının teslimat tarihi için sipariş verebilir

### 2. Fabrika API'leri

#### Sipariş Dinleme API'si
```
GET /orders/api/factory/orders/?token=factory_printer_2024
```

**Parametreler:**
- `token`: Güvenlik token'ı (factory_printer_2024)
- `last_check`: Son kontrol zamanı (isteğe bağlı)

**Yanıt:**
```json
{
  "orders": [
    {
      "id": 123,
      "order_number": "VEG-20250801-001",
      "branch_name": "Vega",
      "customer_name": "Vega - Günlük Sipariş",
      "delivery_date": "2025-08-02",
      "status": "Beklemede",
      "notes": "Özel talepler",
      "created_at": "2025-08-01T10:30:00Z",
      "total_amount": 250.00,
      "items": [
        {
          "product_name": "FISTIK ÇİKOLATA SİYAH",
          "quantity": 5.0,
          "unit": "Adet",
          "notes": "Özel not"
        }
      ],
      "created_by": "Vega Şube Müdürü"
    }
  ],
  "count": 1,
  "timestamp": "2025-08-01T10:45:00Z"
}
```

#### Yazdırma İşaretleme API'si
```
POST /orders/api/factory/mark-printed/
```

**Gövde:**
```json
{
  "token": "factory_printer_2024",
  "order_id": 123
}
```

### 3. Fabrika Yazıcı Programı (`fabrika_yazici_program.py`)

#### 🖥️ GUI Özellikleri
- **Kontrol Paneli**: Başlat/Durdur butonları
- **Durum Göstergesi**: Bağlantı durumu ve servis durumu
- **İstatistikler**: Toplam sipariş, yazdırılan sayısı
- **Sipariş Tablosu**: Aktif siparişler listesi
- **Log Alanı**: Gerçek zamanlı aktivite logu
- **Ayarlar**: API URL, token ve kontrol aralığı ayarları

#### 🔧 Çalışma Mantığı
1. **API Dinleme**: 30 saniyede bir API'yi kontrol eder
2. **Yeni Sipariş Algılama**: Daha önce işlenmemiş siparişleri bulur
3. **Otomatik Yazdırma**: Yeni siparişleri yazıcıdan çıkarır
4. **Durum Güncelleme**: API'ye yazdırıldığını bildirir
5. **Log Tutma**: Tüm işlemleri kayıt altına alır

#### 📄 Yazıcı Çıktısı Formatı
```
==================================================
      TATO PASTA & BAKLAVA
        FABRİKA SİPARİŞİ
==================================================

Sipariş No    : VEG-20250801-001
Şube          : Vega
Teslimat      : 02.08.2025
Sipariş Zamanı: 01.08.2025 13:30
Sipariş Veren : Vega Şube Müdürü
Notlar        : Yarının siparişi

--------------------------------------------------
                 ÜRÜNLER
--------------------------------------------------
FISTIK ÇİKOLATA SİYAH                    5 Adet
KROKANLI ÇİKOLATA                        3 Adet
VİŞNE ÇİKOLATALI                         2 Adet
--------------------------------------------------
Toplam Ürün   : 10 adet
Toplam Tutar  : ₺250.00

==================================================
Yazdırma: 01.08.2025 13:45:30
==================================================
```

## 🚀 Kurulum ve Kullanım

### 1. Sistem Gereksinimleri
- Python 3.8+
- tkinter (GUI için)
- requests kütüphanesi
- İnternet bağlantısı

### 2. Fabrika Bilgisayarında Kurulum

#### Windows:
```cmd
# Gerekli kütüphaneleri yükle
pip install requests

# Programı indir
# fabrika_yazici_program.py dosyasını fabrika bilgisayarına kopyala

# Programı çalıştır
python fabrika_yazici_program.py
```

#### Linux:
```bash
# Gerekli paketleri yükle
sudo apt-get install python3-tk python3-pip
pip3 install requests

# Programı çalıştır
python3 fabrika_yazici_program.py
```

### 3. İlk Kurulum
1. **Bağlantı Testi**: "🔍 Bağlantı Testi" butonuna tıklayın
2. **Ayarlar**: Gerekirse "⚙️ Ayarlar"dan API URL'sini güncelleyin
3. **Servisi Başlatın**: "▶️ Başlat" butonuna tıklayın
4. **Kontrol**: Log alanından işlemleri takip edin

### 4. Günlük Kullanım

#### Şube Müdürleri İçin:
1. https://siparis.tatopastabaklava.com adresine gidin
2. Kullanıcı adı ve şifrenizle giriş yapın
3. "Günlük Sipariş Oluştur" sayfasından sipariş verin
4. Ürünleri seçin ve miktarları belirleyin
5. "Siparişi Gönder" butonuna tıklayın

#### Fabrika Personeli İçin:
1. Bilgisayarı açın ve programı başlatın
2. "▶️ Başlat" butonuna tıklayın
3. Sistem otomatik olarak yeni siparişleri yazdıracak
4. Yazdırılan siparişleri takip edin
5. Gerekirse "🔄 Yenile" ile manuel kontrol yapın

## 🔧 Sorun Giderme

### Bağlantı Sorunları
- **🔴 Bağlantı Yok**: İnternet bağlantınızı kontrol edin
- **🔴 API Hatası**: Token'ın doğru olduğunu kontrol edin
- **🔴 Hata**: Sunucu adresinin doğru olduğunu kontrol edin

### Yazdırma Sorunları
- **Yazıcı Bulunamadı**: Yazıcı bağlantısını kontrol edin
- **İzin Hatası**: Yazıcı izinlerini kontrol edin
- **Kağıt Sıkışması**: Yazıcı durumunu kontrol edin

### Program Sorunları
- **Program Açılmıyor**: Python kurulumunu kontrol edin
- **GUI Görünmüyor**: tkinter kurulumunu kontrol edin
- **Yavaş Çalışma**: İnternet hızınızı kontrol edin

## 📞 Destek

Sorunlarınız için:
1. Log dosyasını kontrol edin: `fabrika_log.txt`
2. Yazdırılan dosyaları kontrol edin: `yazdirilanlar/` klasörü
3. Sistem yöneticisine başvurun

## 🔄 Güncelleme Notları

### v1.0 (01.08.2025)
- ✅ İlk sistem kurulumu tamamlandı
- ✅ API'ler oluşturuldu
- ✅ Fabrika yazıcı programı geliştirildi
- ✅ Test siparişleri başarıyla yazdırıldı

### Gelecek Sürümler
- 🔮 Yazıcı entegrasyonu geliştirilecek
- 🔮 Raporlama özellikleri eklenecek
- 🔮 Bildirim sistemi geliştirilecek
- 🔮 Mobil uygulama desteği

## 📊 İstatistikler

- **Aktarılan Ürün Sayısı**: 27 pasta çeşidi
- **Oluşturulan Şube**: 3 (Vega, Çarşı, Fabrika)
- **Oluşturulan Kullanıcı**: 2 şube müdürü
- **API Endpoint**: 2 fabrika API'si
- **Test Sipariş**: ✅ Başarılı

---

🎉 **Sistem başarıyla kurulmuş ve çalışır durumda!**