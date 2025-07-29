# Pastane İşletme Yönetim Sistemi

![Python](https://img.shields.io/badge/python-v3.11+-blue.svg)
![Django](https://img.shields.io/badge/django-v4.2+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

Kapsamlı pastane/fırın işletmesi yönetim sistemi. 1 imalat merkezi + 2 şube yapısında çalışan, modern web teknolojileri ile geliştirilmiş sistem.

## 🚀 Özellikler

### 📋 Sipariş Yönetimi
- Mobil-uyumlu sipariş formu
- Ürün arama ve filtreleme
- Toplu sipariş verme
- Geçmiş sipariş kopyalama
- Sipariş durum takibi
- Otomatik sipariş numaralandırma

### 📦 Stok Yönetimi
- Gerçek zamanlı stok seviyeleri
- Otomatik stok düşüşü (satış/imha)
- Düşük stok uyarıları
- Stok transfer işlemleri
- Barkod entegrasyonu
- Detaylı stok hareketleri

### 🏭 Üretim Yönetimi
- Üretim planlaması
- Parti takibi
- Reçete yönetimi
- Kalite kontrol
- Maliyet hesaplama
- Verim analizi

### 📊 Raporlama
- Dashboard ile genel bakış
- Satış raporları
- Üretim raporları
- Stok raporları
- İmha raporları

### 👥 Kullanıcı Yönetimi
- Rol tabanlı erişim kontrolü
- Şube bazlı yetkilendirme
- Detaylı kullanıcı profilleri
- Çalışan takibi

## 🛠 Teknoloji Stack

- **Backend**: Django 4.2 + Django REST Framework
- **Frontend**: Django Templates + HTMX + Alpine.js + Tailwind CSS
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Task Queue**: Celery + Redis
- **Web Server**: Nginx + Gunicorn
- **Deployment**: Docker + Docker Compose

## 📦 Kurulum

### Gereksinimler
- Python 3.11+
- Docker & Docker Compose
- Git

### 1. Projeyi Klonlayın
```bash
git clone https://github.com/your-username/pastane-yonetim.git
cd pastane-yonetim
```

### 2. Environment Dosyasını Oluşturun
```bash
cp env_example.txt .env
```

`.env` dosyasını düzenleyerek gerekli ayarları yapın:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://postgres:password@localhost:5432/bakery_db
REDIS_URL=redis://localhost:6379/0
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 3. Geliştirme Ortamı

#### Docker ile (Önerilen)
```bash
# Development ortamını başlat
docker-compose -f docker-compose.dev.yml up -d

# Süperadmin kullanıcısı oluştur
docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser

# Örnek veri yükle (isteğe bağlı)
docker-compose -f docker-compose.dev.yml exec web python manage.py loaddata fixtures/sample_data.json
```

#### Manuel Kurulum
```bash
# Virtual environment oluştur
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Bağımlılıkları yükle
pip install -r requirements.txt

# Veritabanı migrasyonları
python manage.py migrate

# Static dosyaları topla
python manage.py collectstatic

# Süperadmin oluştur
python manage.py createsuperuser

# Geliştirme sunucusunu başlat
python manage.py runserver
```

### 4. Prodüksiyon Ortamı

```bash
# Prodüksiyon ortamını başlat
docker-compose up -d

# SSL sertifikalarını ayarla (isteğe bağlı)
# ./docker/nginx/ssl/ dizinine sertifikalarınızı koyun
```

## 🖥 Kullanım

### Ana Dashboard
- **URL**: `http://localhost:8000`
- Modern, responsive dashboard
- Gerçek zamanlı veri güncellemeleri
- Hızlı işlem butonları

### Admin Panel
- **URL**: `http://localhost:8000/admin`
- Gelişmiş admin arayüzü
- Tüm modeller için CRUD işlemleri
- Filtreleme ve arama özellikleri

### API Endpoints
Tüm işlemler için RESTful API endpoints mevcuttur:

```
GET    /api/orders/          # Sipariş listesi
POST   /api/orders/          # Yeni sipariş
GET    /api/orders/{id}/     # Sipariş detayı
PUT    /api/orders/{id}/     # Sipariş güncelle

GET    /api/inventory/       # Stok listesi
POST   /api/inventory/       # Stok ekle
GET    /api/products/        # Ürün listesi

GET    /api/production/      # Üretim planları
POST   /api/production/      # Yeni üretim planı

GET    /api/reports/         # Raporlar
```

## 👥 Kullanıcı Rolleri

### Sistem Yöneticisi (admin)
- Tüm sisteme erişim
- Kullanıcı yönetimi
- Sistem ayarları

### Genel Müdür (manager)
- Tüm şubelere erişim
- Raporları görüntüleme
- Onay işlemleri

### İmalat Sorumlusu (production_manager)
- Üretim planlaması
- Kalite kontrol
- Stok yönetimi

### Şube Sorumlusu (branch_manager)
- Kendi şubesi için tüm işlemler
- Sipariş yönetimi
- Personel yönetimi

### Kasiyer (cashier)
- Sipariş alma
- Satış işlemleri
- Temel stok görüntüleme

## 📱 Mobil Uyumluluk

Sistem tamamen responsive tasarıma sahiptir:
- 📱 Mobile-first yaklaşım
- 📱 Touch-friendly arayüz
- 📱 Offline çalışma desteği (PWA)

## 🔧 Özelleştirme

### Yeni Modül Ekleme
```python
# myapp/models.py
from django.db import models

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    # ... diğer alanlar

# myapp/serializers.py
from rest_framework import serializers
from .models import MyModel

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'
```

### Template Özelleştirme
Templates `templates/` dizininde bulunur:
- `base.html` - Ana şablon
- `dashboard.html` - Dashboard
- App-specific templates her app dizininde

## 🧪 Test

```bash
# Tüm testleri çalıştır
python manage.py test

# Belirli bir app'i test et
python manage.py test orders

# Coverage raporu
coverage run --source='.' manage.py test
coverage report
coverage html
```

## 📈 Performans

### Optimizasyon İpuçları
- Redis cache kullanımı
- Database query optimizasyonu
- Static dosya sıkıştırma
- Nginx gzip compression

### Monitoring
- Django Debug Toolbar (development)
- Logging yapılandırması
- Performance metrikleri

## 🔒 Güvenlik

- CSRF koruması
- XSS koruması
- SQL injection koruması
- Rate limiting
- Input validasyonu
- HTTPS zorunluluğu (prodüksiyon)

## 🚀 Deployment

### Docker ile Deployment
```bash
# Production build
docker-compose up -d

# SSL sertifikası yenile
docker-compose exec nginx nginx -s reload

# Backup oluştur
docker-compose exec db pg_dump -U bakery_user bakery_db > backup.sql
```

### Manuel Deployment
1. Sunucuya kod transferi
2. Bağımlılıkları yükle
3. Environment değişkenlerini ayarla
4. Database migrasyonları
5. Static dosyaları topla
6. Nginx ve Gunicorn ayarları

## 📚 Dokümantasyon

### API Dokümantasyonu
- **URL**: `http://localhost:8000/api/docs/`
- Swagger/OpenAPI formatında
- Tüm endpoints için örnekler

### Kod Dokümantasyonu
```bash
# Docstring'lerden HTML dokümantasyon oluştur
sphinx-build -b html docs/ docs/_build/
```

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

### Kod Standartları
- Black formatter kullanın
- Flake8 linting
- Type hints ekleyin
- Docstring yazın
- Test yazın

## 📋 TODO

- [ ] Mobile app (React Native)
- [ ] Barkod okuyucu entegrasyonu
- [ ] E-fatura entegrasyonu
- [ ] WhatsApp bildirimleri
- [ ] Müşteri paneli
- [ ] Muhasebe entegrasyonu
- [ ] Multi-dil desteği
- [ ] Real-time notifications

## 🐛 Hata Bildirimi

Hata bulduğunuzda lütfen [Issues](https://github.com/your-username/pastane-yonetim/issues) sayfasından bildirin.

## 📄 Lisans

Bu proje [MIT License](LICENSE) ile lisanslanmıştır.

## 👨‍💻 Geliştirici

**Pastane Yönetim Sistemi** - [GitHub](https://github.com/your-username)

## 🙏 Teşekkürler

- Django ve REST Framework topluluğu
- HTMX ve Alpine.js geliştiricileri
- Tailwind CSS ekibi
- Açık kaynak topluluğu

---

**⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!** 