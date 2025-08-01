#!/usr/bin/env python3
"""
Tato Pasta & Baklava - Fabrika Yazıcı Programı
Uzaktaki üretim tesisi için sipariş dinleme ve yazdırma uygulaması
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import json
import threading
import time
from datetime import datetime, timezone
import os
import sys
from typing import List, Dict, Optional
import webbrowser

class FabrikaYaziciProgrami:
    """Fabrika yazıcı ana programı"""
    
    def __init__(self):
        # Konfigürasyon
        self.api_url = "https://siparis.tatopastabaklava.com"
        self.token = "factory_printer_2024"
        self.check_interval = 30  # 30 saniyede bir kontrol
        
        # Durum değişkenleri
        self.is_running = False
        self.last_check_time = None
        self.processed_orders = set()
        
        # Ana pencere oluştur
        self.root = tk.Tk()
        self.root.title("Tato Pasta & Baklava - Fabrika Yazıcı Sistemi")
        self.root.geometry("1200x800")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Stil ayarları
        style = ttk.Style()
        style.theme_use('clam')
        
        # Arayüzü oluştur
        self.create_widgets()
        
        # Log dosyası
        self.log_file = "fabrika_log.txt"
        
        self.log_message("🏭 Fabrika Yazıcı Programı başlatıldı")
        self.log_message(f"🔗 API URL: {self.api_url}")
    
    def create_widgets(self):
        """Arayüz bileşenlerini oluştur"""
        
        # Ana başlık
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(title_frame, text="🏭 TATO PASTA & BAKLAVA", 
                 font=('Arial', 16, 'bold')).pack()
        ttk.Label(title_frame, text="Fabrika Yazıcı Sistemi", 
                 font=('Arial', 12)).pack()
        
        # Kontrol paneli
        control_frame = ttk.LabelFrame(self.root, text="📋 Kontrol Paneli")
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Kontrol butonları
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.start_btn = ttk.Button(button_frame, text="▶️ Başlat", 
                                   command=self.start_service, style='success.TButton')
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(button_frame, text="⏹️ Durdur", 
                                  command=self.stop_service, style='danger.TButton')
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        self.test_btn = ttk.Button(button_frame, text="🔍 Bağlantı Testi", 
                                  command=self.test_connection)
        self.test_btn.pack(side=tk.LEFT, padx=5)
        
        self.refresh_btn = ttk.Button(button_frame, text="🔄 Yenile", 
                                     command=self.manual_check)
        self.refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Ayarlar butonu
        ttk.Button(button_frame, text="⚙️ Ayarlar", 
                  command=self.show_settings).pack(side=tk.RIGHT, padx=5)
        
        # Durum bilgileri
        status_frame = ttk.Frame(control_frame)
        status_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.status_label = ttk.Label(status_frame, text="⏸️ Durduruldu", 
                                     font=('Arial', 10, 'bold'))
        self.status_label.pack(side=tk.LEFT)
        
        self.connection_label = ttk.Label(status_frame, text="🔴 Bağlantı Yok", 
                                         font=('Arial', 10))
        self.connection_label.pack(side=tk.RIGHT)
        
        # İstatistikler
        stats_frame = ttk.LabelFrame(self.root, text="📊 İstatistikler")
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        stats_inner = ttk.Frame(stats_frame)
        stats_inner.pack(fill=tk.X, padx=5, pady=5)
        
        self.total_orders_label = ttk.Label(stats_inner, text="Toplam Sipariş: 0")
        self.total_orders_label.pack(side=tk.LEFT, padx=10)
        
        self.printed_orders_label = ttk.Label(stats_inner, text="Yazdırılan: 0")
        self.printed_orders_label.pack(side=tk.LEFT, padx=10)
        
        self.last_check_label = ttk.Label(stats_inner, text="Son Kontrol: -")
        self.last_check_label.pack(side=tk.LEFT, padx=10)
        
        # Siparişler tablosu
        orders_frame = ttk.LabelFrame(self.root, text="📦 Aktif Siparişler")
        orders_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Tablo oluştur
        columns = ('siparis_no', 'sube', 'tarih', 'urun_sayisi', 'tutar', 'durum')
        self.orders_tree = ttk.Treeview(orders_frame, columns=columns, show='headings', height=10)
        
        # Sütun başlıkları
        self.orders_tree.heading('siparis_no', text='Sipariş No')
        self.orders_tree.heading('sube', text='Şube')
        self.orders_tree.heading('tarih', text='Teslimat Tarihi')
        self.orders_tree.heading('urun_sayisi', text='Ürün Sayısı')
        self.orders_tree.heading('tutar', text='Tutar')
        self.orders_tree.heading('durum', text='Durum')
        
        # Sütun genişlikleri
        self.orders_tree.column('siparis_no', width=120)
        self.orders_tree.column('sube', width=100)
        self.orders_tree.column('tarih', width=100)
        self.orders_tree.column('urun_sayisi', width=80)
        self.orders_tree.column('tutar', width=80)
        self.orders_tree.column('durum', width=100)
        
        # Scrollbar ekle
        scrollbar = ttk.Scrollbar(orders_frame, orient=tk.VERTICAL, command=self.orders_tree.yview)
        self.orders_tree.configure(yscrollcommand=scrollbar.set)
        
        self.orders_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Çift tıklama eventi
        self.orders_tree.bind('<Double-1>', self.on_order_double_click)
        
        # Sağ tık menüsü
        self.create_context_menu()
        
        # Log alanı
        log_frame = ttk.LabelFrame(self.root, text="📝 Aktivite Logu")
        log_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Alt durum çubuğu
        self.status_bar = ttk.Label(self.root, text="Program hazır", relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_context_menu(self):
        """Sağ tık menüsü oluştur"""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="🖨️ Tekrar Yazdır", command=self.reprint_order)
        self.context_menu.add_command(label="📋 Detayları Göster", command=self.show_order_details)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="✅ Yazdırıldı İşaretle", command=self.mark_as_printed)
        
        self.orders_tree.bind("<Button-3>", self.show_context_menu)
    
    def show_context_menu(self, event):
        """Sağ tık menüsünü göster"""
        item = self.orders_tree.selection()[0] if self.orders_tree.selection() else None
        if item:
            self.context_menu.post(event.x_root, event.y_root)
    
    def log_message(self, message: str):
        """Log mesajı ekle"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        # GUI'ye ekle
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        
        # Dosyaya kaydet
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{datetime.now().isoformat()}] {message}\n")
        except:
            pass
        
        # Durum çubuğunu güncelle
        self.status_bar.config(text=message)
    
    def test_connection(self):
        """API bağlantısını test et"""
        self.log_message("🔍 API bağlantısı test ediliyor...")
        
        def test_in_thread():
            try:
                url = f"{self.api_url}/orders/api/factory/orders/"
                params = {'token': self.token}
                
                response = requests.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    count = data.get('count', 0)
                    
                    self.root.after(0, lambda: self.connection_label.config(text="🟢 Bağlı"))
                    self.root.after(0, lambda: self.log_message(f"✅ Bağlantı başarılı! {count} sipariş mevcut"))
                    
                    # Siparişleri güncelle
                    self.root.after(0, lambda: self.update_orders(data.get('orders', [])))
                    
                else:
                    self.root.after(0, lambda: self.connection_label.config(text="🔴 Hata"))
                    self.root.after(0, lambda: self.log_message(f"❌ API hatası: {response.status_code}"))
                    
            except Exception as e:
                self.root.after(0, lambda: self.connection_label.config(text="🔴 Bağlantı Yok"))
                self.root.after(0, lambda: self.log_message(f"❌ Bağlantı hatası: {str(e)}"))
        
        threading.Thread(target=test_in_thread, daemon=True).start()
    
    def start_service(self):
        """Servisi başlat"""
        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_label.config(text="▶️ Çalışıyor")
        
        self.log_message("🚀 Servis başlatıldı")
        
        # Arka plan thread'i başlat
        self.service_thread = threading.Thread(target=self.service_loop, daemon=True)
        self.service_thread.start()
    
    def stop_service(self):
        """Servisi durdur"""
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_label.config(text="⏸️ Durduruldu")
        self.connection_label.config(text="🔴 Bağlantı Yok")
        
        self.log_message("⏹️ Servis durduruldu")
    
    def service_loop(self):
        """Ana servis döngüsü"""
        while self.is_running:
            try:
                self.check_for_new_orders()
                time.sleep(self.check_interval)
            except Exception as e:
                self.root.after(0, lambda: self.log_message(f"❌ Servis hatası: {str(e)}"))
                time.sleep(5)
    
    def check_for_new_orders(self):
        """Yeni siparişleri kontrol et"""
        try:
            url = f"{self.api_url}/orders/api/factory/orders/"
            params = {'token': self.token}
            
            if self.last_check_time:
                params['last_check'] = self.last_check_time.isoformat()
            
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                orders = data.get('orders', [])
                
                # GUI güncellemelerini ana thread'de yap
                self.root.after(0, lambda: self.connection_label.config(text="🟢 Bağlı"))
                self.root.after(0, lambda: self.process_new_orders(orders))
                
                # Son kontrol zamanını güncelle
                self.last_check_time = datetime.now(timezone.utc)
                self.root.after(0, lambda: self.last_check_label.config(
                    text=f"Son Kontrol: {self.last_check_time.strftime('%H:%M:%S')}"
                ))
                
            else:
                self.root.after(0, lambda: self.connection_label.config(text="🔴 API Hatası"))
                self.root.after(0, lambda: self.log_message(f"❌ API hatası: {response.status_code}"))
                
        except Exception as e:
            self.root.after(0, lambda: self.connection_label.config(text="🔴 Bağlantı Yok"))
            self.root.after(0, lambda: self.log_message(f"❌ Bağlantı hatası: {str(e)}"))
    
    def process_new_orders(self, orders: List[Dict]):
        """Yeni siparişleri işle"""
        new_orders = [order for order in orders if order['id'] not in self.processed_orders]
        
        if new_orders:
            self.log_message(f"🆕 {len(new_orders)} yeni sipariş alındı")
            
            for order in new_orders:
                self.print_order(order)
                self.processed_orders.add(order['id'])
        
        # Tüm siparişleri güncelle
        self.update_orders(orders)
        
        # İstatistikleri güncelle
        self.update_statistics(orders)
    
    def update_orders(self, orders: List[Dict]):
        """Siparişler tablosunu güncelle"""
        # Mevcut verileri temizle
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)
        
        # Yeni verileri ekle
        for order in orders:
            values = (
                order['order_number'],
                order['branch_name'],
                self.format_date(order['delivery_date']),
                len(order['items']),
                f"₺{order['total_amount']:.0f}",
                "✅ Yazdırıldı" if order['id'] in self.processed_orders else "⏳ Bekliyor"
            )
            
            item = self.orders_tree.insert('', tk.END, values=values)
            
            # Renk kodlaması
            if order['id'] in self.processed_orders:
                self.orders_tree.set(item, 'durum', "✅ Yazdırıldı")
            else:
                self.orders_tree.set(item, 'durum', "⏳ Bekliyor")
    
    def update_statistics(self, orders: List[Dict]):
        """İstatistikleri güncelle"""
        total = len(orders)
        printed = len([o for o in orders if o['id'] in self.processed_orders])
        
        self.total_orders_label.config(text=f"Toplam Sipariş: {total}")
        self.printed_orders_label.config(text=f"Yazdırılan: {printed}")
    
    def print_order(self, order: Dict):
        """Siparişi yazdır"""
        try:
            self.log_message(f"🖨️ Yazdırılıyor: {order['order_number']} - {order['branch_name']}")
            
            # Yazdırma formatını hazırla
            formatted_text = self.format_order_for_printing(order)
            
            # Konsola yazdır (test için)
            print("\n" + "="*60)
            print("YAZICI ÇIKTISI:")
            print(formatted_text)
            print("="*60)
            
            # Dosyaya kaydet
            self.save_order_to_file(order, formatted_text)
            
            # API'ye yazdırıldığını bildir
            self.mark_order_printed_api(order['id'])
            
            self.log_message(f"✅ Başarıyla yazdırıldı: {order['order_number']}")
            
        except Exception as e:
            self.log_message(f"❌ Yazdırma hatası: {str(e)}")
    
    def format_order_for_printing(self, order: Dict) -> str:
        """Siparişi yazdırma formatına dönüştür"""
        lines = []
        lines.append("=" * 50)
        lines.append("      TATO PASTA & BAKLAVA")
        lines.append("        FABRİKA SİPARİŞİ")
        lines.append("=" * 50)
        lines.append("")
        
        lines.append(f"Sipariş No    : {order['order_number']}")
        lines.append(f"Şube          : {order['branch_name']}")
        lines.append(f"Teslimat      : {self.format_date(order['delivery_date'])}")
        lines.append(f"Sipariş Zamanı: {self.format_datetime(order['created_at'])}")
        lines.append(f"Sipariş Veren : {order['created_by']}")
        
        if order['notes']:
            lines.append(f"Notlar        : {order['notes']}")
        
        lines.append("")
        lines.append("-" * 50)
        lines.append("                 ÜRÜNLER")
        lines.append("-" * 50)
        
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
        lines.append("=" * 50)
        lines.append(f"Yazdırma: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
        lines.append("=" * 50)
        lines.append("")
        
        return "\n".join(lines)
    
    def save_order_to_file(self, order: Dict, content: str):
        """Siparişi dosyaya kaydet"""
        try:
            os.makedirs('yazdirilanlar', exist_ok=True)
            filename = f"yazdirilanlar/siparis_{order['order_number']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
                
        except Exception as e:
            self.log_message(f"⚠️ Dosya kaydetme hatası: {str(e)}")
    
    def mark_order_printed_api(self, order_id: int):
        """API'ye siparişin yazdırıldığını bildir"""
        try:
            url = f"{self.api_url}/orders/api/factory/mark-printed/"
            data = {'token': self.token, 'order_id': order_id}
            
            response = requests.post(url, json=data, timeout=10)
            
            if response.status_code == 200:
                self.log_message(f"✅ API'de işaretlendi: {order_id}")
            else:
                self.log_message(f"⚠️ API işaretleme hatası: {response.status_code}")
                
        except Exception as e:
            self.log_message(f"❌ API işaretleme hatası: {str(e)}")
    
    def format_date(self, date_str: str) -> str:
        """Tarih formatla"""
        try:
            date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return date.strftime('%d.%m.%Y')
        except:
            return date_str
    
    def format_datetime(self, datetime_str: str) -> str:
        """Tarih-saat formatla"""
        try:
            dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
            return dt.strftime('%d.%m.%Y %H:%M')
        except:
            return datetime_str
    
    def manual_check(self):
        """Manuel kontrol"""
        self.log_message("🔄 Manuel kontrol yapılıyor...")
        threading.Thread(target=self.check_for_new_orders, daemon=True).start()
    
    def show_settings(self):
        """Ayarlar penceresini göster"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("⚙️ Ayarlar")
        settings_window.geometry("400x300")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # API URL
        ttk.Label(settings_window, text="API URL:").pack(pady=5)
        url_entry = ttk.Entry(settings_window, width=50)
        url_entry.insert(0, self.api_url)
        url_entry.pack(pady=5)
        
        # Token
        ttk.Label(settings_window, text="Token:").pack(pady=5)
        token_entry = ttk.Entry(settings_window, width=50)
        token_entry.insert(0, self.token)
        token_entry.pack(pady=5)
        
        # Kontrol aralığı
        ttk.Label(settings_window, text="Kontrol Aralığı (saniye):").pack(pady=5)
        interval_entry = ttk.Entry(settings_window, width=20)
        interval_entry.insert(0, str(self.check_interval))
        interval_entry.pack(pady=5)
        
        # Kaydet butonu
        def save_settings():
            self.api_url = url_entry.get()
            self.token = token_entry.get()
            try:
                self.check_interval = int(interval_entry.get())
            except:
                self.check_interval = 30
            
            settings_window.destroy()
            self.log_message("⚙️ Ayarlar kaydedildi")
        
        ttk.Button(settings_window, text="💾 Kaydet", command=save_settings).pack(pady=20)
    
    def on_order_double_click(self, event):
        """Sipariş çift tıklandığında"""
        self.show_order_details()
    
    def show_order_details(self):
        """Sipariş detaylarını göster"""
        selection = self.orders_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        order_number = self.orders_tree.item(item)['values'][0]
        
        # Detay penceresi aç
        details_window = tk.Toplevel(self.root)
        details_window.title(f"📋 Sipariş Detayları - {order_number}")
        details_window.geometry("600x400")
        
        # Detay metni (basit örnek)
        details_text = scrolledtext.ScrolledText(details_window)
        details_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        details_text.insert(tk.END, f"Sipariş No: {order_number}\n")
        details_text.insert(tk.END, "Detaylı bilgiler yükleniyor...\n")
    
    def reprint_order(self):
        """Siparişi tekrar yazdır"""
        selection = self.orders_tree.selection()
        if selection:
            order_number = self.orders_tree.item(selection[0])['values'][0]
            self.log_message(f"🖨️ Tekrar yazdırılıyor: {order_number}")
    
    def mark_as_printed(self):
        """Manuel olarak yazdırıldı işaretle"""
        selection = self.orders_tree.selection()
        if selection:
            order_number = self.orders_tree.item(selection[0])['values'][0]
            self.log_message(f"✅ Manuel işaretlendi: {order_number}")
    
    def on_closing(self):
        """Program kapatılırken"""
        if self.is_running:
            self.stop_service()
        
        self.log_message("👋 Program kapatılıyor...")
        self.root.destroy()
    
    def run(self):
        """Programı çalıştır"""
        self.root.mainloop()


def main():
    """Ana fonksiyon"""
    try:
        app = FabrikaYaziciProgrami()
        app.run()
    except Exception as e:
        messagebox.showerror("Hata", f"Program başlatılamadı: {str(e)}")


if __name__ == "__main__":
    main()