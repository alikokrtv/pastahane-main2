# Pasta Sipariş Sistemi - Deployment Rehberi

## 🚀 Local Geliştirme Kurulumu

### 1. Sistem Hazırlığı
```bash
# Proje klasörüne gidin
cd pastahane-main

# Virtual environment oluşturun (opsiyonel)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Gerekli paketleri yükleyin
pip install -r requirements.txt
```

### 2. Veritabanı Ayarları
- MySQL 8.0+ kurulumunu yapın
- Root kullanıcısı için şifre: `255223`
- Veritabanı: `viapos_local`

```sql
CREATE DATABASE viapos_local CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Django Kurulumu
```bash
# Migrationları çalıştırın
python manage.py migrate

# Ürünleri Excel'den aktarın
python import_products_multi_db.py

# Test kullanıcıları oluşturun
python create_test_user.py

# Development server'ı başlatın
python manage.py runserver 8000
```

### 4. Test Kullanıcıları
- **Şube Müdürü**: `sube1` / `123456`
- **Admin**: `admin` / `admin123`

### 5. Erişim URL'leri
- Ana sayfa: http://localhost:8000
- Admin panel: http://localhost:8000/admin
- Şube sipariş oluşturma: http://localhost:8000/orders/branch/create/
- Şube sipariş listesi: http://localhost:8000/orders/branch/

## 🌐 Coolify Production Deployment

### 1. Environment Variables
Coolify'de aşağıdaki environment variable'ları ayarlayın:

```env
DEBUG=False
USE_COOLIFY=true
SECRET_KEY=production-secret-key-here
ALLOWED_HOSTS=siparis.tatopastabaklava.com,yourdomain.com
DATABASE_URL=mysql://user:password@host:port/dbname
```

### 2. Git Hazırlık
```bash
# Git repository'sini hazırlayın
git add .
git commit -m "Local development setup complete with product import"
git push origin main
```

### 3. Coolify Ayarları
1. GitHub repository'sini Coolify'e bağlayın
2. Environment variables'ları ayarlayın
3. MySQL database service'ini ekleyin
4. Deploy işlemini başlatın

### 4. Production Database Setup
Coolify'de deployment sonrası:
```bash
# Migrations
python manage.py migrate

# Ürünleri tekrar aktarın (production DB'ye)
python import_products_multi_db.py

# Admin kullanıcısı oluşturun
python manage.py createsuperuser
```

## 📋 Kullanım Rehberi

### Şube Müdürü İş Akışı
1. Sisteme giriş yapın (sube1/123456)
2. "Günlük Sipariş Oluştur" sayfasına gidin
3. Ürünleri seçin ve miktarları belirleyin
4. Teslimat tarihini seçin
5. Sipariş notlarını ekleyin
6. Siparişi oluşturun

### Admin İş Akışı
1. Admin paneline giriş yapın
2. Siparişleri takip edin
3. Üretim planlaması yapın
4. Raporları görüntüleyin

## 🔧 Önemli Notlar

### Veritabanı Bağlantıları
Sistem otomatik olarak en iyi veritabanını seçer:
- Local development: `viapos_local`
- Production: Coolify MySQL
- Fallback: ViaPos remote database

### Güvenlik
- Production'da `DEBUG=False` olmalı
- `SECRET_KEY` güvenli olmalı
- HTTPS kullanın
- Database şifrelerini güvenli tutun

### Monitoring
- Django log'ları: `logs/django.log`
- Database connection test: `python test_database_connections.py`
- System health check: `python manage.py check --deploy`

## 🐛 Troubleshooting

### Database Connection Issues
```bash
# Veritabanı bağlantılarını test edin
python test_database_connections.py
```

### Import Issues
```bash
# Ürünleri tekrar aktarın
python import_products_multi_db.py
```

### Permission Issues
- Branch kullanıcılarının şube ataması olmalı
- Admin kullanıcıları staff/superuser olmalı

## 📞 Destek
Sorun yaşadığınızda:
1. Log dosyalarını kontrol edin
2. Database bağlantılarını test edin
3. Migration durumunu kontrol edin