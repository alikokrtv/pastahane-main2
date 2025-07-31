# Coolify Deployment Rehberi

## 🚀 Coolify'de Ayarlanacak Environment Variables

Coolify'de projenizin **Environment Variables** bölümüne şunları ekleyin:

```env
# Production ayarları
DEBUG=False
USE_COOLIFY=true

# Güvenlik
SECRET_KEY=coolify-production-secret-key-buraya-yaz

# Domain ayarları
ALLOWED_HOSTS=siparis.tatopastabaklava.com,*.tatopastabaklava.com

# Database (Coolify otomatik ayarlayacak)
DATABASE_URL=mysql://mysql:password@host:3306/database

# CORS ayarları (frontend varsa)
CORS_ALLOWED_ORIGINS=https://siparis.tatopastabaklava.com
```

## 📋 Deployment Sonrası Yapılacaklar

### 1. Database Migration
```bash
python manage.py migrate
```

### 2. Ürünleri Coolify Database'ine Aktar
```bash
python import_products_multi_db.py
```

### 3. Test Kullanıcısı Oluştur
```bash
python create_test_user.py
```

### 4. Static Files Collect
```bash
python manage.py collectstatic --noinput
```

## 🔧 Database Bağlantı Mantığı

Sistem akıllı şekilde ayarlandı:

- **Local Development**: `viapos_local` kullanır
- **Coolify Production**: `USE_COOLIFY=true` olduğunda Coolify MySQL kullanır
- **Otomatik Fallback**: Bağlantı sorunu varsa alternatif database'lere geçer

## 🌐 Test Adresleri

Deploy sonrası test etmek için:

- **Ana Sayfa**: https://siparis.tatopastabaklava.com
- **Login**: Otomatik yönlendirilecek
- **Admin**: https://siparis.tatopastabaklava.com/admin
- **Şube Sipariş**: Giriş sonrası otomatik yönlendirilecek

## 👥 Test Kullanıcıları

```
Şube Müdürü: sube1 / 123456
Admin: admin / admin123
```

## 🐛 Sorun Giderme

### Database Connection Test
```bash
python test_database_connections.py
```

### Log Kontrolü
```bash
tail -f logs/django.log
```

### System Check
```bash
python manage.py check --deploy
```

## ✅ Başarı Kontrolleri

1. ✅ Site açılıyor
2. ✅ Login zorunlu
3. ✅ Ürünler görünüyor
4. ✅ + - butonları çalışıyor
5. ✅ Sipariş oluşturuluyor
6. ✅ Fiyat bilgisi yok

## 🔄 Güncelleme Süreci

Değişiklik yapıldığında:

1. Local'de test et
2. Git commit + push
3. Coolify otomatik deploy eder
4. Gerekirse migration çalıştır

## 🎯 Sistem Özellikleri

- ✅ Multi-database support
- ✅ Otomatik authentication
- ✅ Fiyatsız sipariş sistemi
- ✅ Excel ürün aktarımı
- ✅ Branch manager yetkileri
- ✅ Responsive tasarım
- ✅ Production ready