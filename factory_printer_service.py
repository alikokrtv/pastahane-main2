#!/usr/bin/env python3
"""
Fabrika Yazıcı Servisi
Coolify'daki sipariş sistemini dinleyip yeni siparişleri yazıcıdan çıkarır.
"""

import time
import requests
import json
import sys
from datetime import datetime, timezone
from typing import List, Dict, Optional
import logging

# Loglama ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('factory_printer.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Konfigürasyon
API_BASE_URL = "https://siparis.tatopastabaklava.com"
FACTORY_TOKEN = "factory_printer_2024"
CHECK_INTERVAL = 30  # 30 saniyede bir kontrol et
PRINTER_NAME = "POS Yazıcı"  # Yazıcı adı

class FactoryPrinterService:
    """Fabrika yazıcı servisi"""
    
    def __init__(self):
        self.last_check_time = None
        self.printed_orders = set()
        logger.info("🏭 Fabrika Yazıcı Servisi başlatıldı")
        logger.info(f"📡 API URL: {API_BASE_URL}")
        logger.info(f"🖨️  Yazıcı: {PRINTER_NAME}")
        logger.info(f"⏱️  Kontrol aralığı: {CHECK_INTERVAL} saniye")
    
    def get_new_orders(self) -> List[Dict]:
        """API'den yeni siparişleri al"""
        try:
            url = f"{API_BASE_URL}/orders/api/factory/orders/"
            params = {
                'token': FACTORY_TOKEN
            }
            
            # Son kontrol zamanını ekle
            if self.last_check_time:
                params['last_check'] = self.last_check_time.isoformat()
            
            logger.debug(f"📡 API çağrısı yapılıyor: {url}")
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                orders = data.get('orders', [])
                logger.info(f"✅ {len(orders)} yeni sipariş alındı")
                return orders
            elif response.status_code == 401:
                logger.error("❌ Yetkilendirme hatası - Token geçersiz")
                return []
            else:
                logger.error(f"❌ API hatası: {response.status_code} - {response.text}")
                return []
                
        except requests.exceptions.ConnectionError:
            logger.error("❌ İnternet bağlantı hatası")
            return []
        except requests.exceptions.Timeout:
            logger.error("❌ API isteği zaman aşımına uğradı")
            return []
        except Exception as e:
            logger.error(f"❌ Beklenmeyen hata: {e}")
            return []
    
    def format_order_for_printing(self, order: Dict) -> str:
        """Sipariş verilerini yazdırma formatına dönüştür"""
        lines = []
        lines.append("=" * 50)
        lines.append("      TATO PASTA & BAKLAVA")
        lines.append("        FABRİKA SİPARİŞİ")
        lines.append("=" * 50)
        lines.append("")
        
        # Sipariş bilgileri
        lines.append(f"Sipariş No    : {order['order_number']}")
        lines.append(f"Şube          : {order['branch_name']}")
        lines.append(f"Müşteri       : {order['customer_name']}")
        lines.append(f"Teslimat      : {self.format_date(order['delivery_date'])}")
        lines.append(f"Sipariş Zamanı: {self.format_datetime(order['created_at'])}")
        lines.append(f"Durum         : {order['status']}")
        lines.append(f"Sipariş Veren : {order['created_by']}")
        
        if order['notes']:
            lines.append(f"Notlar        : {order['notes']}")
        
        lines.append("")
        lines.append("-" * 50)
        lines.append("                 ÜRÜNLER")
        lines.append("-" * 50)
        
        # Ürün listesi
        total_items = 0
        for item in order['items']:
            product_line = f"{item['product_name']:<30} {item['quantity']:>8} {item['unit']}"
            lines.append(product_line)
            
            if item['notes']:
                lines.append(f"  Not: {item['notes']}")
            
            total_items += item['quantity']
        
        lines.append("-" * 50)
        lines.append(f"Toplam Ürün   : {total_items} adet")
        lines.append(f"Toplam Tutar  : ₺{order['total_amount']:.2f}")
        lines.append("")
        lines.append("⚠️  HAZIRLIK ÖNCELİĞİ:")
        
        # Teslimat tarihine göre öncelik belirle
        delivery_date = datetime.fromisoformat(order['delivery_date'].replace('Z', '+00:00'))
        now = datetime.now(timezone.utc)
        hours_until_delivery = (delivery_date - now).total_seconds() / 3600
        
        if hours_until_delivery <= 24:
            lines.append("🔴 ACİL - 24 SAAT İÇİNDE TESLİMAT!")
        elif hours_until_delivery <= 48:
            lines.append("🟡 NORMAL - 48 SAAT İÇİNDE TESLİMAT")
        else:
            lines.append("🟢 STANDART - TESLİMAT TARİHİ UZAK")
        
        lines.append("")
        lines.append("=" * 50)
        lines.append(f"Yazdırma Zamanı: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
        lines.append("=" * 50)
        lines.append("")
        lines.append("")  # Kağıdı kesmek için boş satırlar
        lines.append("")
        
        return "\n".join(lines)
    
    def format_date(self, date_str: str) -> str:
        """Tarih formatını düzenle"""
        try:
            date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return date.strftime('%d.%m.%Y')
        except:
            return date_str
    
    def format_datetime(self, datetime_str: str) -> str:
        """Tarih-saat formatını düzenle"""
        try:
            dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
            return dt.strftime('%d.%m.%Y %H:%M')
        except:
            return datetime_str
    
    def print_order(self, order: Dict) -> bool:
        """Siparişi yazıcıdan çıkar"""
        try:
            # Sipariş formatını hazırla
            formatted_order = self.format_order_for_printing(order)
            
            # Konsola yazdır (test için)
            print("\n" + "🖨️ " * 20)
            print("YAZICI ÇIKTISI:")
            print(formatted_order)
            print("🖨️ " * 20 + "\n")
            
            # Gerçek yazıcı entegrasyonu için:
            # Windows'ta: os.system(f'print /D:{PRINTER_NAME} temp_order.txt')
            # Linux'ta: os.system(f'lp -d {PRINTER_NAME} temp_order.txt')
            
            # Geçici dosya oluştur ve yazdır (isteğe bağlı)
            self.save_to_file(order, formatted_order)
            
            logger.info(f"🖨️  Sipariş yazdırıldı: {order['order_number']}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Yazdırma hatası: {e}")
            return False
    
    def save_to_file(self, order: Dict, formatted_content: str):
        """Siparişi dosyaya kaydet (backup için)"""
        try:
            filename = f"siparis_{order['order_number']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(f"printed_orders/{filename}", 'w', encoding='utf-8') as f:
                f.write(formatted_content)
            logger.debug(f"💾 Sipariş dosyaya kaydedildi: {filename}")
        except Exception as e:
            logger.warning(f"⚠️  Dosya kaydetme hatası: {e}")
    
    def mark_order_printed(self, order_id: int) -> bool:
        """Siparişin yazdırıldığını API'ye bildir"""
        try:
            url = f"{API_BASE_URL}/orders/api/factory/mark-printed/"
            data = {
                'token': FACTORY_TOKEN,
                'order_id': order_id
            }
            
            response = requests.post(url, json=data, timeout=10)
            
            if response.status_code == 200:
                logger.info(f"✅ Sipariş yazdırıldı olarak işaretlendi: {order_id}")
                return True
            else:
                logger.error(f"❌ API işaretleme hatası: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ İşaretleme hatası: {e}")
            return False
    
    def process_orders(self, orders: List[Dict]):
        """Siparişleri işle"""
        for order in orders:
            order_id = order['id']
            
            # Daha önce yazdırılmış mı kontrol et
            if order_id in self.printed_orders:
                continue
            
            logger.info(f"🆕 Yeni sipariş: {order['order_number']} - {order['branch_name']}")
            
            # Siparişi yazdır
            if self.print_order(order):
                # Yazdırıldı olarak işaretle
                if self.mark_order_printed(order_id):
                    self.printed_orders.add(order_id)
                else:
                    logger.warning(f"⚠️  Sipariş yazdırıldı ama API'de işaretlenemedi: {order['order_number']}")
            else:
                logger.error(f"❌ Sipariş yazdırılamadı: {order['order_number']}")
    
    def run(self):
        """Ana servis döngüsü"""
        logger.info("🚀 Servis başlatılıyor...")
        
        # Printed orders klasörünü oluştur
        import os
        os.makedirs('printed_orders', exist_ok=True)
        
        while True:
            try:
                logger.info("🔍 Yeni siparişler kontrol ediliyor...")
                
                # Yeni siparişleri al
                orders = self.get_new_orders()
                
                # Siparişleri işle
                if orders:
                    self.process_orders(orders)
                else:
                    logger.info("📭 Yeni sipariş yok")
                
                # Son kontrol zamanını güncelle
                self.last_check_time = datetime.now(timezone.utc)
                
                # Bekleme
                logger.info(f"😴 {CHECK_INTERVAL} saniye bekleniyor...")
                time.sleep(CHECK_INTERVAL)
                
            except KeyboardInterrupt:
                logger.info("⛔ Servis kullanıcı tarafından durduruldu")
                break
            except Exception as e:
                logger.error(f"❌ Beklenmeyen hata: {e}")
                time.sleep(5)  # Hata durumunda kısa bekleme


def main():
    """Ana fonksiyon"""
    print("🏭 Tato Pasta & Baklava - Fabrika Yazıcı Servisi")
    print("=" * 60)
    print("Bu servis Coolify'daki sipariş sistemini dinler")
    print("ve yeni siparişleri otomatik olarak yazıcıdan çıkarır.")
    print("=" * 60)
    print()
    
    # Test bağlantısı
    print("🔗 API bağlantısı test ediliyor...")
    try:
        response = requests.get(f"{API_BASE_URL}/orders/api/factory/orders/?token={FACTORY_TOKEN}", timeout=10)
        if response.status_code == 200:
            print("✅ API bağlantısı başarılı!")
        else:
            print(f"❌ API bağlantı hatası: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")
        return
    
    print()
    
    # Servisi başlat
    service = FactoryPrinterService()
    service.run()


if __name__ == "__main__":
    main()