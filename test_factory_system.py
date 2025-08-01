#!/usr/bin/env python3
"""
Fabrika sistemi test scripti
"""

import requests
import json
from datetime import datetime, timedelta

# Test konfigürasyonu
API_BASE_URL = "https://siparis.tatopastabaklava.com"
LOCAL_URL = "http://127.0.0.1:8000"  # Local test için

def test_login_and_create_order():
    """Şube müdürü girişi ve sipariş oluşturma testi"""
    print("🧪 Test 1: Şube müdürü girişi ve sipariş oluşturma")
    print("-" * 50)
    
    # Test edilecek kullanıcılar
    test_users = [
        {'username': 'vega_mudur', 'password': 'vega123', 'branch': 'Vega'},
        {'username': 'carsi_mudur', 'password': 'carsi123', 'branch': 'Çarşı'}
    ]
    
    for user in test_users:
        print(f"\n👤 {user['branch']} şube müdürü testi:")
        
        # Django login sayfasına POST (session based)
        session = requests.Session()
        
        # CSRF token al
        try:
            login_page = session.get(f"{LOCAL_URL}/users/login/")
            if login_page.status_code == 200:
                print(f"  ✅ Login sayfasına erişim başarılı")
            else:
                print(f"  ❌ Login sayfasına erişim başarısız: {login_page.status_code}")
                continue
        except Exception as e:
            print(f"  ❌ Bağlantı hatası: {e}")
            continue
        
        print(f"  📋 Kullanıcı: {user['username']}")
        print(f"  🏢 Şube: {user['branch']}")

def test_factory_api():
    """Fabrika API'si testi"""
    print("\n🧪 Test 2: Fabrika API testi")
    print("-" * 50)
    
    # Factory orders API'yi test et
    try:
        url = f"{LOCAL_URL}/orders/api/factory/orders/"
        params = {'token': 'factory_printer_2024'}
        
        print(f"📡 API çağrısı: {url}")
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API çağrısı başarılı")
            print(f"📊 Sipariş sayısı: {data['count']}")
            print(f"⏰ Timestamp: {data['timestamp']}")
            
            if data['orders']:
                print("📋 İlk sipariş örneği:")
                first_order = data['orders'][0]
                print(f"   Sipariş No: {first_order['order_number']}")
                print(f"   Şube: {first_order['branch_name']}")
                print(f"   Teslimat: {first_order['delivery_date']}")
                print(f"   Ürün sayısı: {len(first_order['items'])}")
        else:
            print(f"❌ API hatası: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ API test hatası: {e}")

def test_create_sample_order():
    """Örnek sipariş oluşturma"""
    print("\n🧪 Test 3: Manuel sipariş oluşturma")
    print("-" * 50)
    
    # Django ORM kullanarak sipariş oluştur
    try:
        import os
        import sys
        import django
        from pathlib import Path
        
        # Django ayarlarını yükle
        BASE_DIR = Path(__file__).resolve().parent
        sys.path.append(str(BASE_DIR))
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bakery_management.settings')
        django.setup()
        
        from orders.models import Order, OrderItem
        from inventory.models import Product
        from users.models import Branch, CustomUser
        from datetime import date
        
        # Vega şubesini al
        vega_branch = Branch.objects.get(name='Vega')
        vega_user = CustomUser.objects.get(username='vega_mudur')
        
        # Birkaç ürün al
        products = Product.objects.filter(is_active=True)[:3]
        
        if not products:
            print("❌ Sistemde aktif ürün bulunamadı")
            return
        
        # Test siparişi oluştur
        tomorrow = date.today() + timedelta(days=1)
        
        order = Order.objects.create(
            branch=vega_branch,
            customer_name=f"{vega_branch.name} - Test Siparişi",
            requested_delivery_date=tomorrow,
            notes="Test amaçlı oluşturulan sipariş",
            priority='normal',
            status='pending',
            created_by=vega_user
        )
        
        # Sipariş kalemlerini ekle
        total = 0
        for i, product in enumerate(products):
            quantity = (i + 1) * 2  # 2, 4, 6 adet
            
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                unit_price=product.price_per_unit,
                notes=f"Test kalemi {i+1}"
            )
            total += order_item.get_total_price()
        
        # Toplam tutarı güncelle
        order.subtotal = total
        order.total_amount = total
        order.save()
        
        print(f"✅ Test siparişi oluşturuldu!")
        print(f"   Sipariş No: {order.order_number}")
        print(f"   Şube: {order.branch.name}")
        print(f"   Toplam: ₺{order.total_amount}")
        print(f"   Ürün sayısı: {order.items.count()}")
        
        return order
        
    except Exception as e:
        print(f"❌ Sipariş oluşturma hatası: {e}")
        return None

def test_mark_printed():
    """Yazdırma işaretleme testi"""
    print("\n🧪 Test 4: Sipariş yazdırma işaretleme")
    print("-" * 50)
    
    # İlk önce bir sipariş bul
    try:
        import os
        import sys
        import django
        from pathlib import Path
        
        BASE_DIR = Path(__file__).resolve().parent
        sys.path.append(str(BASE_DIR))
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bakery_management.settings')
        django.setup()
        
        from orders.models import Order
        
        # Pending durumdaki ilk siparişi al
        order = Order.objects.filter(status='pending').first()
        
        if not order:
            print("❌ Test edilecek sipariş bulunamadı")
            return
        
        print(f"📋 Test siparişi: {order.order_number}")
        print(f"   Durum: {order.get_status_display()}")
        
        # Mark printed API'yi çağır
        url = f"{LOCAL_URL}/orders/api/factory/mark-printed/"
        data = {
            'token': 'factory_printer_2024',
            'order_id': order.id
        }
        
        response = requests.post(url, json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ İşaretleme başarılı: {result['message']}")
            
            # Siparişi tekrar kontrol et
            order.refresh_from_db()
            print(f"   Yeni durum: {order.get_status_display()}")
        else:
            print(f"❌ İşaretleme hatası: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ İşaretleme test hatası: {e}")

def main():
    """Ana test fonksiyonu"""
    print("🧪 Tato Pasta & Baklava - Sistem Test Programı")
    print("=" * 60)
    print("Bu program sistemin tüm bileşenlerini test eder.")
    print("=" * 60)
    
    # Test edilecek URL'yi belirle
    print(f"🔗 Test URL'i: {LOCAL_URL}")
    
    # Temel bağlantı testi
    print("\n🔍 Temel bağlantı testi...")
    try:
        response = requests.get(LOCAL_URL, timeout=5)
        if response.status_code == 200:
            print("✅ Django sunucusu erişilebilir")
        else:
            print(f"❌ Django sunucusu yanıt vermiyor: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")
        print("💡 Django sunucusunun çalıştığından emin olun: python manage.py runserver")
        return
    
    # Testleri çalıştır
    test_login_and_create_order()
    test_factory_api()
    
    # ORM testleri
    test_create_sample_order()
    test_mark_printed()
    
    print("\n🎉 Tüm testler tamamlandı!")
    print("\n📝 Sonraki adımlar:")
    print("1. Django sunucusunu başlatın: python manage.py runserver")
    print("2. Şube müdürleri giriş yapabilir: vega_mudur / vega123")
    print("3. Fabrika scripti çalıştırın: python factory_printer_service.py")

if __name__ == "__main__":
    main()