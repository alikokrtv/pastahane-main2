#!/usr/bin/env python3
"""
Tato Pasta & Baklava - Gelişmiş Fabrika Yazıcı Programı
Otomatik yazıcı algılama, durum kontrolü ve akıllı yazdırma özellikleri
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
import tempfile
import subprocess
from typing import List, Dict, Optional
import webbrowser

# Windows yazıcı desteği için
try:
    import win32print
    import win32api
    PRINTER_SUPPORT = True
except ImportError:
    PRINTER_SUPPORT = False
    print("⚠️ win32print modülü bulunamadı. Yazıcı özellikleri sınırlı olacak.")

class PrinterManager:
    """Yazıcı yönetim sistemi"""
    
    def __init__(self):
        self.available_printers = []
        self.selected_printer = None
        self.printer_status = {}
        
    def scan_printers(self):
        """Sistemdeki yazıcıları tara"""
        self.available_printers.clear()
        self.printer_status.clear()
        
        if not PRINTER_SUPPORT:
            # Fallback: Basit sistem komutu ile
            self.available_printers = ["Varsayılan Yazıcı"]
            self.printer_status["Varsayılan Yazıcı"] = "Bilinmiyor"
            return self.available_printers
        
        try:
            # Windows yazıcılarını listele
            printers = win32print.EnumPrinters(2)
            
            for printer in printers:
                printer_name = printer[2]  # Yazıcı adı
                self.available_printers.append(printer_name)
                
                # Yazıcı durumunu kontrol et
                status = self.check_printer_status(printer_name)
                self.printer_status[printer_name] = status
            
            # Varsayılan yazıcıyı belirle
            try:
                default_printer = win32print.GetDefaultPrinter()
                if default_printer in self.available_printers:
                    self.selected_printer = default_printer
            except:
                if self.available_printers:
                    self.selected_printer = self.available_printers[0]
                    
        except Exception as e:
            print(f"Yazıcı tarama hatası: {e}")
            self.available_printers = ["Varsayılan Yazıcı"]
            self.printer_status["Varsayılan Yazıcı"] = "Hata"
        
        return self.available_printers
    
    def check_printer_status(self, printer_name):
        """Yazıcı durumunu kontrol et"""
        if not PRINTER_SUPPORT:
            return "Bilinmiyor"
        
        try:
            handle = win32print.OpenPrinter(printer_name)
            printer_info = win32print.GetPrinter(handle, 2)
            win32print.ClosePrinter(handle)
            
            status = printer_info['Status']
            
            # Durum kodlarını çevir
            if status == 0:
                return "✅ Hazır"
            elif status & win32print.PRINTER_STATUS_OFFLINE:
                return "🔴 Çevrimdışı"
            elif status & win32print.PRINTER_STATUS_ERROR:
                return "❌ Hata"
            elif status & win32print.PRINTER_STATUS_PAPER_JAM:
                return "📄 Kağıt Sıkışması"
            elif status & win32print.PRINTER_STATUS_PAPER_OUT:
                return "📭 Kağıt Yok"
            elif status & win32print.PRINTER_STATUS_DOOR_OPEN:
                return "🚪 Kapak Açık"
            else:
                return f"⚠️ Durum: {status}"
                
        except Exception as e:
            return f"❌ Hata: {str(e)[:20]}"
    
    def test_printer(self, printer_name):
        """Yazıcı test et"""
        try:
            # Test metni oluştur
            test_content = f"""
YAZICI TEST ÇIKTISI
==================
Tarih: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
Yazıcı: {printer_name}

Bu bir test yazdırmasıdır.
Eğer bu metni okuyabiliyorsanız
yazıcınız düzgün çalışıyor.

TATO PASTA & BAKLAVA
Fabrika Yazıcı Sistemi
==================
"""
            
            # Geçici dosya oluştur
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
                f.write(test_content)
                temp_file = f.name
            
            # Yazdır
            success = self.print_file(temp_file, printer_name)
            
            # Geçici dosyayı sil
            try:
                os.unlink(temp_file)
            except:
                pass
            
            return success
            
        except Exception as e:
            print(f"Test yazdırma hatası: {e}")
            return False
    
    def print_file(self, file_path, printer_name=None):
        """Dosyayı yazdır"""
        if not printer_name:
            printer_name = self.selected_printer
        
        if not printer_name:
            return False
        
        try:
            if PRINTER_SUPPORT:
                # Windows API ile yazdır
                win32api.ShellExecute(
                    0, "print", file_path, f'/d:"{printer_name}"', ".", 0
                )
            else:
                # Fallback: Sistem komutu
                if os.name == 'nt':  # Windows
                    subprocess.run(['print', f'/D:{printer_name}', file_path], shell=True)
                else:  # Linux
                    subprocess.run(['lp', '-d', printer_name, file_path])
            
            return True
            
        except Exception as e:
            print(f"Yazdırma hatası: {e}")
            return False
    
    def print_text(self, text, printer_name=None):
        """Metin yazdır"""
        try:
            # Geçici dosya oluştur
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
                f.write(text)
                temp_file = f.name
            
            # Yazdır
            success = self.print_file(temp_file, printer_name)
            
            # Geçici dosyayı sil
            try:
                os.unlink(temp_file)
            except:
                pass
            
            return success
            
        except Exception as e:
            print(f"Metin yazdırma hatası: {e}")
            return False

class GelismiFabrikaYaziciProgrami:
    """Gelişmiş fabrika yazıcı ana programı"""
    
    def __init__(self):
        # Konfigürasyon
        self.api_url = "https://siparis.tatopastabaklava.com"
        self.token = "factory_printer_2024"
        self.check_interval = 30  # 30 saniyede bir kontrol
        
        # Durum değişkenleri
        self.is_running = False
        self.last_check_time = None
        self.processed_orders = set()
        
        # Yazıcı yöneticisi
        self.printer_manager = PrinterManager()
        
        # Ana pencere oluştur
        self.root = tk.Tk()
        self.root.title("Tato Pasta & Baklava - Gelişmiş Fabrika Yazıcı Sistemi")
        self.root.geometry("1400x900")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Stil ayarları
        style = ttk.Style()
        style.theme_use('clam')
        
        # Arayüzü oluştur
        self.create_widgets()
        
        # Log dosyası
        self.log_file = "fabrika_log.txt"
        
        self.log_message("🏭 Gelişmiş Fabrika Yazıcı Programı başlatıldı")
        self.log_message(f"🔗 API URL: {self.api_url}")
        
        # Yazıcıları tara
        self.refresh_printers()
    
    def create_widgets(self):
        """Arayüz bileşenlerini oluştur"""
        
        # Ana notebook (sekmeler)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Sekmeler oluştur
        self.create_main_tab()
        self.create_printer_tab()
        self.create_settings_tab()
        self.create_logs_tab()
        
        # Alt durum çubuğu
        self.status_bar = ttk.Label(self.root, text="Program hazır", relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_main_tab(self):
        """Ana kontrol sekmesi"""
        main_frame = ttk.Frame(self.notebook)
        self.notebook.add(main_frame, text="📋 Ana Kontrol")
        
        # Başlık
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(title_frame, text="🏭 TATO PASTA & BAKLAVA", 
                 font=('Arial', 16, 'bold')).pack()
        ttk.Label(title_frame, text="Gelişmiş Fabrika Yazıcı Sistemi", 
                 font=('Arial', 12)).pack()
        
        # Kontrol paneli
        control_frame = ttk.LabelFrame(main_frame, text="📋 Kontrol Paneli")
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Sol taraf - kontrol butonları
        left_control = ttk.Frame(control_frame)
        left_control.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        button_frame = ttk.Frame(left_control)
        button_frame.pack(fill=tk.X)
        
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
        
        # Sağ taraf - durum bilgileri
        right_control = ttk.Frame(control_frame)
        right_control.pack(side=tk.RIGHT, padx=5, pady=5)
        
        self.status_label = ttk.Label(right_control, text="⏸️ Durduruldu", 
                                     font=('Arial', 10, 'bold'))
        self.status_label.pack()
        
        self.connection_label = ttk.Label(right_control, text="🔴 Bağlantı Yok", 
                                         font=('Arial', 10))
        self.connection_label.pack()
        
        self.printer_status_label = ttk.Label(right_control, text="🖨️ Yazıcı: Seçilmedi", 
                                             font=('Arial', 10))
        self.printer_status_label.pack()
        
        # İstatistikler
        stats_frame = ttk.LabelFrame(main_frame, text="📊 İstatistikler")
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
        orders_frame = ttk.LabelFrame(main_frame, text="📦 Aktif Siparişler")
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
    
    def create_printer_tab(self):
        """Yazıcı yönetimi sekmesi"""
        printer_frame = ttk.Frame(self.notebook)
        self.notebook.add(printer_frame, text="🖨️ Yazıcı Yönetimi")
        
        # Yazıcı listesi
        printer_list_frame = ttk.LabelFrame(printer_frame, text="📋 Mevcut Yazıcılar")
        printer_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Yazıcı tablosu
        printer_columns = ('name', 'status', 'default')
        self.printer_tree = ttk.Treeview(printer_list_frame, columns=printer_columns, show='headings', height=8)
        
        self.printer_tree.heading('name', text='Yazıcı Adı')
        self.printer_tree.heading('status', text='Durum')
        self.printer_tree.heading('default', text='Varsayılan')
        
        self.printer_tree.column('name', width=300)
        self.printer_tree.column('status', width=150)
        self.printer_tree.column('default', width=100)
        
        self.printer_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Yazıcı kontrol butonları
        printer_control_frame = ttk.Frame(printer_list_frame)
        printer_control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(printer_control_frame, text="🔄 Yazıcıları Tara", 
                  command=self.refresh_printers).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(printer_control_frame, text="🖨️ Test Yazdır", 
                  command=self.test_selected_printer).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(printer_control_frame, text="✅ Seç", 
                  command=self.select_printer).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(printer_control_frame, text="⚙️ Ayarlar", 
                  command=self.printer_settings).pack(side=tk.RIGHT, padx=5)
        
        # Seçili yazıcı bilgisi
        selected_frame = ttk.LabelFrame(printer_frame, text="📌 Seçili Yazıcı")
        selected_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.selected_printer_label = ttk.Label(selected_frame, text="Seçili yazıcı yok", 
                                               font=('Arial', 12, 'bold'))
        self.selected_printer_label.pack(pady=10)
        
        # Test yazdırma alanı
        test_frame = ttk.LabelFrame(printer_frame, text="🧪 Test Yazdırma")
        test_frame.pack(fill=tk.X, padx=10, pady=5)
        
        test_inner = ttk.Frame(test_frame)
        test_inner.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(test_inner, text="Test metni:").pack(anchor=tk.W)
        
        self.test_text = tk.Text(test_inner, height=4, wrap=tk.WORD)
        self.test_text.pack(fill=tk.X, pady=5)
        self.test_text.insert('1.0', "Bu bir test yazdırmasıdır.\nTarih: " + datetime.now().strftime('%d.%m.%Y %H:%M:%S'))
        
        test_btn_frame = ttk.Frame(test_inner)
        test_btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(test_btn_frame, text="🖨️ Test Yazdır", 
                  command=self.test_print_custom).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(test_btn_frame, text="📄 Standart Test", 
                  command=self.test_print_standard).pack(side=tk.LEFT, padx=5)
    
    def create_settings_tab(self):
        """Ayarlar sekmesi"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="⚙️ Ayarlar")
        
        # API ayarları
        api_frame = ttk.LabelFrame(settings_frame, text="🔗 API Ayarları")
        api_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # API URL
        ttk.Label(api_frame, text="API URL:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.url_entry = ttk.Entry(api_frame, width=50)
        self.url_entry.insert(0, self.api_url)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Token
        ttk.Label(api_frame, text="Güvenlik Token:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.token_entry = ttk.Entry(api_frame, width=50, show="*")
        self.token_entry.insert(0, self.token)
        self.token_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Kontrol aralığı
        ttk.Label(api_frame, text="Kontrol Aralığı (saniye):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.interval_entry = ttk.Entry(api_frame, width=20)
        self.interval_entry.insert(0, str(self.check_interval))
        self.interval_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Yazıcı ayarları
        printer_settings_frame = ttk.LabelFrame(settings_frame, text="🖨️ Yazıcı Ayarları")
        printer_settings_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Otomatik yazıcı seçimi
        self.auto_printer_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(printer_settings_frame, text="Otomatik yazıcı seçimi", 
                       variable=self.auto_printer_var).pack(anchor=tk.W, padx=5, pady=5)
        
        # Yazdırma sonrası bekleme
        ttk.Label(printer_settings_frame, text="Yazdırma sonrası bekleme (saniye):").pack(anchor=tk.W, padx=5)
        self.print_delay_entry = ttk.Entry(printer_settings_frame, width=20)
        self.print_delay_entry.insert(0, "2")
        self.print_delay_entry.pack(anchor=tk.W, padx=5, pady=2)
        
        # Kaydet butonu
        ttk.Button(settings_frame, text="💾 Ayarları Kaydet", 
                  command=self.save_settings).pack(pady=20)
    
    def create_logs_tab(self):
        """Log sekmesi"""
        log_frame = ttk.Frame(self.notebook)
        self.notebook.add(log_frame, text="📝 Loglar")
        
        # Log alanı
        log_text_frame = ttk.LabelFrame(log_frame, text="📋 Aktivite Logu")
        log_text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_text_frame, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Log kontrol butonları
        log_control_frame = ttk.Frame(log_frame)
        log_control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(log_control_frame, text="🗑️ Temizle", 
                  command=self.clear_logs).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(log_control_frame, text="💾 Kaydet", 
                  command=self.save_logs).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(log_control_frame, text="📂 Log Klasörü", 
                  command=self.open_log_folder).pack(side=tk.RIGHT, padx=5)
    
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
    
    def refresh_printers(self):
        """Yazıcıları tara ve listele"""
        self.log_message("🔄 Yazıcılar taranıyor...")
        
        def scan_in_thread():
            printers = self.printer_manager.scan_printers()
            
            # GUI güncellemesini ana thread'de yap
            self.root.after(0, lambda: self.update_printer_list(printers))
        
        threading.Thread(target=scan_in_thread, daemon=True).start()
    
    def update_printer_list(self, printers):
        """Yazıcı listesini güncelle"""
        # Mevcut verileri temizle
        for item in self.printer_tree.get_children():
            self.printer_tree.delete(item)
        
        # Yeni verileri ekle
        for printer in printers:
            status = self.printer_manager.printer_status.get(printer, "Bilinmiyor")
            is_default = "✅" if printer == self.printer_manager.selected_printer else ""
            
            self.printer_tree.insert('', tk.END, values=(printer, status, is_default))
        
        # Seçili yazıcı bilgisini güncelle
        if self.printer_manager.selected_printer:
            self.selected_printer_label.config(text=f"📌 {self.printer_manager.selected_printer}")
            self.printer_status_label.config(text=f"🖨️ {self.printer_manager.selected_printer}")
        else:
            self.selected_printer_label.config(text="❌ Seçili yazıcı yok")
            self.printer_status_label.config(text="🖨️ Yazıcı: Seçilmedi")
        
        self.log_message(f"✅ {len(printers)} yazıcı bulundu")
    
    def test_selected_printer(self):
        """Seçili yazıcıyı test et"""
        selection = self.printer_tree.selection()
        if not selection:
            messagebox.showwarning("Uyarı", "Lütfen test edilecek yazıcıyı seçin")
            return
        
        item = selection[0]
        printer_name = self.printer_tree.item(item)['values'][0]
        
        self.log_message(f"🧪 Yazıcı test ediliyor: {printer_name}")
        
        def test_in_thread():
            success = self.printer_manager.test_printer(printer_name)
            
            self.root.after(0, lambda: self.show_test_result(printer_name, success))
        
        threading.Thread(target=test_in_thread, daemon=True).start()
    
    def show_test_result(self, printer_name, success):
        """Test sonucunu göster"""
        if success:
            self.log_message(f"✅ Test başarılı: {printer_name}")
            messagebox.showinfo("Test Başarılı", f"Yazıcı test başarılı!\n{printer_name}")
        else:
            self.log_message(f"❌ Test başarısız: {printer_name}")
            messagebox.showerror("Test Başarısız", f"Yazıcı test başarısız!\n{printer_name}\n\nKontrol edilecekler:\n- Yazıcı açık mı?\n- Kağıt var mı?\n- Bağlantı sorunsuz mu?")
    
    def select_printer(self):
        """Yazıcı seç"""
        selection = self.printer_tree.selection()
        if not selection:
            messagebox.showwarning("Uyarı", "Lütfen seçilecek yazıcıyı seçin")
            return
        
        item = selection[0]
        printer_name = self.printer_tree.item(item)['values'][0]
        
        self.printer_manager.selected_printer = printer_name
        self.update_printer_list(self.printer_manager.available_printers)
        
        self.log_message(f"✅ Yazıcı seçildi: {printer_name}")
    
    def test_print_custom(self):
        """Özel test metni yazdır"""
        if not self.printer_manager.selected_printer:
            messagebox.showwarning("Uyarı", "Önce bir yazıcı seçin")
            return
        
        text = self.test_text.get('1.0', tk.END).strip()
        if not text:
            messagebox.showwarning("Uyarı", "Test metni boş olamaz")
            return
        
        self.log_message("🖨️ Özel test yazdırılıyor...")
        
        def print_in_thread():
            success = self.printer_manager.print_text(text)
            self.root.after(0, lambda: self.show_test_result("Özel test", success))
        
        threading.Thread(target=print_in_thread, daemon=True).start()
    
    def test_print_standard(self):
        """Standart test yazdır"""
        if not self.printer_manager.selected_printer:
            messagebox.showwarning("Uyarı", "Önce bir yazıcı seçin")
            return
        
        self.log_message("🖨️ Standart test yazdırılıyor...")
        
        def print_in_thread():
            success = self.printer_manager.test_printer(self.printer_manager.selected_printer)
            self.root.after(0, lambda: self.show_test_result("Standart test", success))
        
        threading.Thread(target=print_in_thread, daemon=True).start()
    
    def printer_settings(self):
        """Yazıcı ayarları penceresi"""
        if not self.printer_manager.selected_printer:
            messagebox.showwarning("Uyarı", "Önce bir yazıcı seçin")
            return
        
        # Yazıcı ayarları penceresini göster
        settings_window = tk.Toplevel(self.root)
        settings_window.title(f"⚙️ {self.printer_manager.selected_printer} Ayarları")
        settings_window.geometry("400x300")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        ttk.Label(settings_window, text=f"Yazıcı: {self.printer_manager.selected_printer}", 
                 font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Durum bilgisi
        status = self.printer_manager.printer_status.get(self.printer_manager.selected_printer, "Bilinmiyor")
        ttk.Label(settings_window, text=f"Durum: {status}").pack(pady=5)
        
        # Test butonu
        ttk.Button(settings_window, text="🧪 Test Yazdır", 
                  command=lambda: self.printer_manager.test_printer(self.printer_manager.selected_printer)).pack(pady=10)
    
    def save_settings(self):
        """Ayarları kaydet"""
        self.api_url = self.url_entry.get()
        self.token = self.token_entry.get()
        
        try:
            self.check_interval = int(self.interval_entry.get())
        except:
            self.check_interval = 30
        
        self.log_message("⚙️ Ayarlar kaydedildi")
        messagebox.showinfo("Ayarlar", "Ayarlar başarıyla kaydedildi!")
    
    def clear_logs(self):
        """Log alanını temizle"""
        self.log_text.delete('1.0', tk.END)
        self.log_message("🗑️ Log alanı temizlendi")
    
    def save_logs(self):
        """Logları dosyaya kaydet"""
        try:
            log_content = self.log_text.get('1.0', tk.END)
            filename = f"log_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(log_content)
            
            self.log_message(f"💾 Loglar kaydedildi: {filename}")
            messagebox.showinfo("Kaydet", f"Loglar başarıyla kaydedildi:\n{filename}")
        except Exception as e:
            messagebox.showerror("Hata", f"Log kaydetme hatası:\n{str(e)}")
    
    def open_log_folder(self):
        """Log klasörünü aç"""
        try:
            os.startfile(os.getcwd())
        except:
            self.log_message("⚠️ Log klasörü açılamadı")
    
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
                    
            except requests.exceptions.ConnectionError:
                self.root.after(0, lambda: self.connection_label.config(text="🔴 Bağlantı Yok"))
                self.root.after(0, lambda: self.log_message("❌ İnternet bağlantı hatası"))
            except requests.exceptions.Timeout:
                self.root.after(0, lambda: self.connection_label.config(text="🔴 Zaman Aşımı"))
                self.root.after(0, lambda: self.log_message("❌ API isteği zaman aşımına uğradı"))
            except Exception as e:
                self.root.after(0, lambda: self.connection_label.config(text="🔴 Hata"))
                self.root.after(0, lambda: self.log_message(f"❌ Beklenmeyen hata: {str(e)}"))
        
        threading.Thread(target=test_in_thread, daemon=True).start()
    
    def start_service(self):
        """Servisi başlat"""
        if not self.printer_manager.selected_printer:
            messagebox.showwarning("Uyarı", "Önce bir yazıcı seçin!")
            return
        
        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_label.config(text="▶️ Çalışıyor")
        
        self.log_message("🚀 Servis başlatıldı")
        self.log_message(f"🖨️ Aktif yazıcı: {self.printer_manager.selected_printer}")
        
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
            
            # Yazıcı kontrolü
            if not self.printer_manager.selected_printer:
                self.log_message("❌ Yazıcı seçilmedi!")
                return
            
            # Yazdırma formatını hazırla
            formatted_text = self.format_order_for_printing(order)
            
            # Konsola yazdır (test için)
            print("\n" + "="*60)
            print("YAZICI ÇIKTISI:")
            print(formatted_text)
            print("="*60)
            
            # Yazıcıdan yazdır
            success = self.printer_manager.print_text(formatted_text)
            
            if success:
                # Dosyaya kaydet
                self.save_order_to_file(order, formatted_text)
                
                # API'ye yazdırıldığını bildir
                self.mark_order_printed_api(order['id'])
                
                self.log_message(f"✅ Başarıyla yazdırıldı: {order['order_number']}")
                
                # Yazdırma sonrası bekleme
                delay = int(self.print_delay_entry.get() or "2")
                time.sleep(delay)
            else:
                self.log_message(f"❌ Yazdırma başarısız: {order['order_number']}")
            
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
        
        # Yazıcı bilgisi
        lines.append(f"Yazıcı        : {self.printer_manager.selected_printer}")
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
        
        # Detay metni
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
        app = GelismiFabrikaYaziciProgrami()
        app.run()
    except Exception as e:
        messagebox.showerror("Hata", f"Program başlatılamadı: {str(e)}")


if __name__ == "__main__":
    main()