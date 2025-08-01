#!/usr/bin/env python3
"""
Tato Pasta & Baklava - ÇALIŞAN Fabrika Yazıcı Programı
Gerçek işlevsellik ile tüm butonlar çalışıyor
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
import platform
from typing import List, Dict, Optional
import webbrowser
import socket

# Windows yazıcı desteği için
try:
    import win32print
    import win32api
    PRINTER_SUPPORT = True
except ImportError:
    PRINTER_SUPPORT = False

class CalisanYaziciYoneticisi:
    """Gerçekten çalışan yazıcı yöneticisi"""
    
    def __init__(self):
        self.available_printers = {}
        self.selected_printer = None
        
    def yazicilari_tara(self):
        """Yazıcıları gerçekten tara"""
        self.available_printers.clear()
        
        try:
            if PRINTER_SUPPORT:
                # Windows yazıcıları
                printers = win32print.EnumPrinters(2)
                for printer in printers:
                    printer_name = printer[2]
                    try:
                        # Yazıcı durumunu kontrol et
                        handle = win32print.OpenPrinter(printer_name)
                        printer_info = win32print.GetPrinter(handle, 2)
                        win32print.ClosePrinter(handle)
                        
                        status = self._durum_cevir(printer_info['Status'])
                        
                        self.available_printers[printer_name] = {
                            'name': printer_name,
                            'status': status,
                            'port': printer_info.get('pPortName', 'Bilinmiyor'),
                            'driver': printer_info.get('pDriverName', 'Bilinmiyor'),
                            'location': printer_info.get('pLocation', 'Yerel'),
                            'is_default': False
                        }
                        
                        # Varsayılan yazıcıyı işaretle
                        try:
                            default = win32print.GetDefaultPrinter()
                            if default == printer_name:
                                self.available_printers[printer_name]['is_default'] = True
                                self.selected_printer = printer_name
                        except:
                            pass
                            
                    except Exception as e:
                        self.available_printers[printer_name] = {
                            'name': printer_name,
                            'status': f'Hata: {str(e)[:20]}',
                            'port': 'Bilinmiyor',
                            'driver': 'Bilinmiyor',
                            'location': 'Bilinmiyor',
                            'is_default': False
                        }
            else:
                # Fallback - basit sistem
                self.available_printers["Varsayılan Yazıcı"] = {
                    'name': "Varsayılan Yazıcı",
                    'status': "Hazır",
                    'port': 'USB',
                    'driver': 'Sistem',
                    'location': 'Yerel',
                    'is_default': True
                }
                self.selected_printer = "Varsayılan Yazıcı"
                
        except Exception as e:
            print(f"Yazıcı tarama hatası: {e}")
            
        return self.available_printers
    
    def _durum_cevir(self, status_code):
        """Windows yazıcı durumunu çevir"""
        if status_code == 0:
            return "✅ Hazır"
        elif status_code & win32print.PRINTER_STATUS_OFFLINE:
            return "🔴 Çevrimdışı"
        elif status_code & win32print.PRINTER_STATUS_ERROR:
            return "❌ Hata"
        elif status_code & win32print.PRINTER_STATUS_PAPER_JAM:
            return "📄 Kağıt Sıkışması"
        elif status_code & win32print.PRINTER_STATUS_PAPER_OUT:
            return "📭 Kağıt Yok"
        elif status_code & win32print.PRINTER_STATUS_DOOR_OPEN:
            return "🚪 Kapak Açık"
        else:
            return f"⚠️ Durum: {status_code}"
    
    def yazici_test_et(self, printer_name):
        """Yazıcıyı gerçekten test et"""
        try:
            test_metni = f"""
TEST YAZDIRMA
=============
Tarih: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
Yazıcı: {printer_name}

Bu bir test yazdırmasıdir.
Eğer bu metni okuyabiliyorsaniz
yazıcınız düzgün çalışıyor.

TATO PASTA & BAKLAVA
Fabrika Yazıcı Sistemi
=============
"""
            
            # Geçici dosya oluştur
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
                f.write(test_metni)
                temp_file = f.name
            
            # Yazdır
            success = self.dosya_yazdir(temp_file, printer_name)
            
            # Geçici dosyayı sil
            try:
                os.unlink(temp_file)
            except:
                pass
            
            return success
            
        except Exception as e:
            print(f"Test yazdırma hatası: {e}")
            return False
    
    def dosya_yazdir(self, file_path, printer_name=None):
        """Dosyayı gerçekten yazdır"""
        if not printer_name:
            printer_name = self.selected_printer
        
        if not printer_name:
            return False
        
        try:
            if PRINTER_SUPPORT:
                # Windows API ile yazdır
                win32api.ShellExecute(0, "print", file_path, f'/d:"{printer_name}"', ".", 0)
            else:
                # Fallback: sistem komutu
                if os.name == 'nt':  # Windows
                    subprocess.run(['notepad', '/p', file_path], shell=True)
                else:  # Linux
                    subprocess.run(['lp', '-d', printer_name, file_path])
            
            return True
            
        except Exception as e:
            print(f"Yazdırma hatası: {e}")
            return False
    
    def metin_yazdir(self, text, printer_name=None):
        """Metni gerçekten yazdır"""
        try:
            # Geçici dosya oluştur
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
                f.write(text)
                temp_file = f.name
            
            # Yazdır
            success = self.dosya_yazdir(temp_file, printer_name)
            
            # Geçici dosyayı sil
            try:
                os.unlink(temp_file)
            except:
                pass
            
            return success
            
        except Exception as e:
            print(f"Metin yazdırma hatası: {e}")
            return False

class CalisanFabrikaYaziciProgram:
    """Gerçekten çalışan fabrika yazıcı programı"""
    
    def __init__(self):
        # Konfigürasyon
        self.api_url = "https://siparis.tatopastabaklava.com"
        self.token = "factory_printer_2024"
        self.check_interval = 5  # 5 saniyede bir kontrol et (çok hızlı)
        
        # Durum değişkenleri
        self.is_running = False
        self.last_check_time = None
        self.processed_orders = set()
        
        # Yazıcı yöneticisi
        self.printer_manager = CalisanYaziciYoneticisi()
        
        # Ana pencere oluştur
        self.root = tk.Tk()
        self.root.title("Tato Pasta & Baklava - ÇALIŞAN Fabrika Yazıcı Sistemi")
        self.root.geometry("1200x800")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Stil ayarları
        style = ttk.Style()
        style.theme_use('clam')
        
        # Arayüzü oluştur
        self.create_widgets()
        
        # Log dosyası
        self.log_file = "calisir_fabrika_log.txt"
        
        self.log_message("🏭 ÇALIŞAN Fabrika Yazıcı Programı başlatıldı")
        self.log_message(f"🔗 API URL: {self.api_url}")
        
        # Yazıcıları otomatik tara
        self.yazicilari_tara()
    
    def create_widgets(self):
        """Arayüz bileşenlerini oluştur"""
        
        # Ana notebook (sekmeler)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Sekmeler oluştur
        self.create_main_tab()
        self.create_printer_tab()
        self.create_test_tab()
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
        ttk.Label(title_frame, text="ÇALIŞAN Fabrika Yazıcı Sistemi", 
                 font=('Arial', 12)).pack()
        
        # Durum paneli
        status_frame = ttk.LabelFrame(main_frame, text="📊 Sistem Durumu")
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        status_inner = ttk.Frame(status_frame)
        status_inner.pack(fill=tk.X, padx=5, pady=5)
        
        # Sol taraf - durum bilgileri
        left_status = ttk.Frame(status_inner)
        left_status.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.printer_status_label = ttk.Label(left_status, text="🖨️ Yazıcı: Seçilmedi", 
                                             font=('Arial', 11, 'bold'))
        self.printer_status_label.pack(anchor=tk.W)
        
        self.connection_label = ttk.Label(left_status, text="🔴 Bağlantı: Test edilmedi", 
                                         font=('Arial', 11))
        self.connection_label.pack(anchor=tk.W)
        
        self.service_status_label = ttk.Label(left_status, text="⏸️ Servis: Durduruldu", 
                                             font=('Arial', 11))
        self.service_status_label.pack(anchor=tk.W)
        
        # Sağ taraf - istatistikler
        right_status = ttk.Frame(status_inner)
        right_status.pack(side=tk.RIGHT, padx=20)
        
        self.total_orders_label = ttk.Label(right_status, text="Toplam Sipariş: 0")
        self.total_orders_label.pack()
        
        self.printed_orders_label = ttk.Label(right_status, text="Yazdırılan: 0")
        self.printed_orders_label.pack()
        
        self.last_check_label = ttk.Label(right_status, text="Son Kontrol: -")
        self.last_check_label.pack()
        
        # Kontrol butonları
        control_frame = ttk.LabelFrame(main_frame, text="🎮 Kontrol Paneli")
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        buttons_frame = ttk.Frame(control_frame)
        buttons_frame.pack(pady=10)
        
        self.start_btn = ttk.Button(buttons_frame, text="▶️ SİSTEMİ BAŞLAT", 
                                   command=self.servisi_baslat)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(buttons_frame, text="⏹️ SİSTEMİ DURDUR", 
                                  command=self.servisi_durdur)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        self.test_btn = ttk.Button(buttons_frame, text="🔍 BAĞLANTI TESTİ", 
                                  command=self.baglanti_test_et)
        self.test_btn.pack(side=tk.LEFT, padx=5)
        
        self.refresh_btn = ttk.Button(buttons_frame, text="🔄 YENİLE", 
                                     command=self.manuel_yenile)
        self.refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Siparişler tablosu
        orders_frame = ttk.LabelFrame(main_frame, text="📦 Üretim Siparişleri")
        orders_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Tablo
        columns = ('siparis_no', 'sube', 'tarih', 'urun_sayisi', 'siparis_veren', 'durum')
        self.orders_tree = ttk.Treeview(orders_frame, columns=columns, show='headings', height=10)
        
        # Sütun başlıkları
        self.orders_tree.heading('siparis_no', text='Sipariş No')
        self.orders_tree.heading('sube', text='Şube')
        self.orders_tree.heading('tarih', text='Teslimat Tarihi')
        self.orders_tree.heading('urun_sayisi', text='Toplam Adet')
        self.orders_tree.heading('siparis_veren', text='Sipariş Veren')
        self.orders_tree.heading('durum', text='Durum')
        
        # Sütun genişlikleri
        self.orders_tree.column('siparis_no', width=120)
        self.orders_tree.column('sube', width=120)
        self.orders_tree.column('tarih', width=100)
        self.orders_tree.column('urun_sayisi', width=90)
        self.orders_tree.column('siparis_veren', width=120)
        self.orders_tree.column('durum', width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(orders_frame, orient=tk.VERTICAL, command=self.orders_tree.yview)
        self.orders_tree.configure(yscrollcommand=scrollbar.set)
        
        self.orders_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_printer_tab(self):
        """Yazıcı yönetimi sekmesi"""
        printer_frame = ttk.Frame(self.notebook)
        self.notebook.add(printer_frame, text="🖨️ Yazıcı Yönetimi")
        
        # Üst kontrol paneli
        control_frame = ttk.LabelFrame(printer_frame, text="🔧 Yazıcı Kontrolleri")
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        control_buttons = ttk.Frame(control_frame)
        control_buttons.pack(pady=10)
        
        ttk.Button(control_buttons, text="🔄 YAZICILARI TARA", 
                  command=self.yazicilari_tara).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_buttons, text="🧪 SEÇİLİ YAZICIYI TEST ET", 
                  command=self.secili_yaziciyi_test_et).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_buttons, text="✅ YAZICI SEÇ", 
                  command=self.yazici_sec).pack(side=tk.LEFT, padx=5)
        
        # Yazıcı listesi
        printers_frame = ttk.LabelFrame(printer_frame, text="📋 Mevcut Yazıcılar")
        printers_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Yazıcı tablosu
        printer_columns = ('name', 'status', 'port', 'driver', 'default')
        self.printer_tree = ttk.Treeview(printers_frame, columns=printer_columns, show='headings', height=10)
        
        self.printer_tree.heading('name', text='Yazıcı Adı')
        self.printer_tree.heading('status', text='Durum')
        self.printer_tree.heading('port', text='Port')
        self.printer_tree.heading('driver', text='Sürücü')
        self.printer_tree.heading('default', text='Varsayılan')
        
        self.printer_tree.column('name', width=200)
        self.printer_tree.column('status', width=120)
        self.printer_tree.column('port', width=100)
        self.printer_tree.column('driver', width=150)
        self.printer_tree.column('default', width=80)
        
        self.printer_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Seçili yazıcı bilgisi
        selected_frame = ttk.LabelFrame(printer_frame, text="📌 Seçili Yazıcı")
        selected_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.selected_printer_label = ttk.Label(selected_frame, text="Seçili yazıcı yok", 
                                               font=('Arial', 12, 'bold'))
        self.selected_printer_label.pack(pady=10)
    
    def create_test_tab(self):
        """Test sekmesi"""
        test_frame = ttk.Frame(self.notebook)
        self.notebook.add(test_frame, text="🧪 Test Merkezi")
        
        # Test butonları
        test_buttons_frame = ttk.LabelFrame(test_frame, text="🎯 Test Seçenekleri")
        test_buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        buttons_grid = ttk.Frame(test_buttons_frame)
        buttons_grid.pack(pady=10)
        
        ttk.Button(buttons_grid, text="⚡ HIZLI TEST", 
                  command=self.hizli_test).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(buttons_grid, text="📄 METİN TESTİ", 
                  command=self.metin_test).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(buttons_grid, text="🖨️ YAZICI DURUMU", 
                  command=self.yazici_durumu_goster).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(buttons_grid, text="🌐 AĞ TESTİ", 
                  command=self.ag_test).pack(side=tk.LEFT, padx=5)
        
        # Özel test alanı
        custom_frame = ttk.LabelFrame(test_frame, text="✏️ Özel Test Metni")
        custom_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(custom_frame, text="Test için yazdırılacak metin:").pack(anchor=tk.W, padx=5, pady=5)
        
        self.custom_text = tk.Text(custom_frame, height=6, wrap=tk.WORD)
        self.custom_text.pack(fill=tk.X, padx=5, pady=5)
        self.custom_text.insert('1.0', f"=======================================\n      TATO PASTA & BAKLAVA\n      ÜRETİM LİSTESİ TEST\n=======================================\n\nTarih: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\nTest Ürünleri:\nBaklava              10 adet\nPasta                 5 adet\nKurabiye             20 adet\n                  --------\nTOPLAM               35 adet\n\n⚠️ Bu bir test yazdırmasıdır.\n\nÜretim Sistemi Test Modu\n=======================================")
        
        ttk.Button(custom_frame, text="🖨️ ÖZEL METNİ YAZDIR", 
                  command=self.ozel_metin_yazdir).pack(pady=5)
        
        # Test sonuçları
        results_frame = ttk.LabelFrame(test_frame, text="📊 Test Sonuçları")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.test_results = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD)
        self.test_results.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def create_settings_tab(self):
        """Ayarlar sekmesi"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="⚙️ Ayarlar")
        
        # API ayarları
        api_frame = ttk.LabelFrame(settings_frame, text="🔗 API Ayarları")
        api_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # URL
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
        
        # Bilgi etiketi
        ttk.Label(api_frame, text="(Önerilen: 5-10 saniye arası)", 
                 font=('Arial', 8), foreground='gray').grid(row=3, column=1, sticky=tk.W, padx=5)
        
        # Kaydet butonu
        ttk.Button(settings_frame, text="💾 AYARLARI KAYDET", 
                  command=self.ayarlari_kaydet).pack(pady=20)
    
    def create_logs_tab(self):
        """Log sekmesi"""
        logs_frame = ttk.Frame(self.notebook)
        self.notebook.add(logs_frame, text="📝 Loglar")
        
        # Log kontrolleri
        log_controls = ttk.Frame(logs_frame)
        log_controls.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(log_controls, text="🔄 LOGLARI YENİLE", 
                  command=self.loglari_yenile).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(log_controls, text="🗑️ LOGLARI TEMİZLE", 
                  command=self.loglari_temizle).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(log_controls, text="💾 DOSYAYA KAYDET", 
                  command=self.loglari_kaydet).pack(side=tk.LEFT, padx=5)
        
        # Log alanı
        log_frame = ttk.LabelFrame(logs_frame, text="📋 Sistem Logları")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    # Gerçek işlevsellik metodları
    def yazicilari_tara(self):
        """Yazıcıları gerçekten tara"""
        self.log_message("🔄 Yazıcılar taranıyor...")
        
        def tara():
            printers = self.printer_manager.yazicilari_tara()
            self.root.after(0, lambda: self.yazici_listesini_guncelle(printers))
        
        threading.Thread(target=tara, daemon=True).start()
    
    def yazici_listesini_guncelle(self, printers):
        """Yazıcı listesini güncelle"""
        # Mevcut verileri temizle
        for item in self.printer_tree.get_children():
            self.printer_tree.delete(item)
        
        # Yeni verileri ekle
        for name, info in printers.items():
            values = (
                name,
                info.get('status', 'Bilinmiyor'),
                info.get('port', 'Bilinmiyor'),
                info.get('driver', 'Bilinmiyor'),
                "✅" if info.get('is_default', False) else ""
            )
            self.printer_tree.insert('', tk.END, values=values)
        
        # Durum güncellemesi
        if self.printer_manager.selected_printer:
            self.selected_printer_label.config(text=f"📌 {self.printer_manager.selected_printer}")
            self.printer_status_label.config(text=f"🖨️ Yazıcı: {self.printer_manager.selected_printer}")
        
        self.log_message(f"✅ {len(printers)} yazıcı bulundu ve listelendi")
    
    def yazici_sec(self):
        """Seçili yazıcıyı aktif et"""
        selection = self.printer_tree.selection()
        if not selection:
            messagebox.showwarning("Uyarı", "Lütfen bir yazıcı seçin")
            return
        
        item = selection[0]
        printer_name = self.printer_tree.item(item)['values'][0]
        
        self.printer_manager.selected_printer = printer_name
        self.selected_printer_label.config(text=f"📌 {printer_name}")
        self.printer_status_label.config(text=f"🖨️ Yazıcı: {printer_name}")
        
        self.log_message(f"✅ Yazıcı seçildi: {printer_name}")
    
    def secili_yaziciyi_test_et(self):
        """Seçili yazıcıyı test et"""
        if not self.printer_manager.selected_printer:
            messagebox.showwarning("Uyarı", "Önce bir yazıcı seçin")
            return
        
        self.log_message(f"🧪 Yazıcı test ediliyor: {self.printer_manager.selected_printer}")
        
        def test_et():
            success = self.printer_manager.yazici_test_et(self.printer_manager.selected_printer)
            self.root.after(0, lambda: self.test_sonucunu_goster(success))
        
        threading.Thread(target=test_et, daemon=True).start()
    
    def test_sonucunu_goster(self, success):
        """Test sonucunu göster"""
        if success:
            self.log_message("✅ Yazıcı test başarılı!")
            messagebox.showinfo("Test Başarılı", "Yazıcı test başarılı!\nTest sayfası yazdırıldı.")
        else:
            self.log_message("❌ Yazıcı test başarısız!")
            messagebox.showerror("Test Başarısız", "Yazıcı test başarısız!\n\nKontrol edilecekler:\n- Yazıcı açık mı?\n- Kağıt var mı?\n- USB bağlantısı sorunsuz mu?")
    
    def baglanti_test_et(self):
        """API bağlantısını test et"""
        self.log_message("🔍 API bağlantısı test ediliyor...")
        
        def test_et():
            try:
                url = f"{self.api_url}/orders/api/factory/orders/"
                params = {'token': self.token, 'days': 7}  # Son 7 günün siparişlerini getir
                
                response = requests.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    count = data.get('count', 0)
                    
                    self.root.after(0, lambda: self.connection_label.config(text="🟢 Bağlantı: Başarılı"))
                    self.root.after(0, lambda: self.log_message(f"✅ API bağlantısı başarılı! {count} sipariş mevcut"))
                    
                    # Siparişleri güncelle
                    orders = data.get('orders', [])
                    self.root.after(0, lambda: self.siparisleri_guncelle(orders))
                    
                else:
                    self.root.after(0, lambda: self.connection_label.config(text="🔴 Bağlantı: API Hatası"))
                    self.root.after(0, lambda: self.log_message(f"❌ API hatası: {response.status_code}"))
                    
            except requests.exceptions.ConnectionError:
                self.root.after(0, lambda: self.connection_label.config(text="🔴 Bağlantı: İnternet Yok"))
                self.root.after(0, lambda: self.log_message("❌ İnternet bağlantı hatası"))
            except requests.exceptions.Timeout:
                self.root.after(0, lambda: self.connection_label.config(text="🔴 Bağlantı: Zaman Aşımı"))
                self.root.after(0, lambda: self.log_message("❌ API isteği zaman aşımına uğradı"))
            except Exception as e:
                self.root.after(0, lambda: self.connection_label.config(text="🔴 Bağlantı: Hata"))
                self.root.after(0, lambda: self.log_message(f"❌ Beklenmeyen hata: {str(e)}"))
        
        threading.Thread(target=test_et, daemon=True).start()
    
    def siparisleri_guncelle(self, orders):
        """Siparişler tablosunu güncelle"""
        # Mevcut verileri temizle
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)
        
        # Yeni verileri ekle
        for order in orders:
            # Toplam ürün adedi hesapla
            total_quantity = sum(item['quantity'] for item in order['items'])
            
            values = (
                order['order_number'],
                order['branch_name'],
                self.format_date(order['delivery_date']),
                f"{total_quantity:.0f} adet",
                order['created_by'],
                "✅ Üretildi" if order['id'] in self.processed_orders else "⏳ Üretim Bekliyor"
            )
            self.orders_tree.insert('', tk.END, values=values)
        
        # İstatistikleri güncelle
        total = len(orders)
        printed = len([o for o in orders if o['id'] in self.processed_orders])
        
        self.total_orders_label.config(text=f"Toplam Sipariş: {total}")
        self.printed_orders_label.config(text=f"Üretildi: {printed}")
    
    def servisi_baslat(self):
        """Ana servisi başlat"""
        if not self.printer_manager.selected_printer:
            messagebox.showwarning("Uyarı", "Önce bir yazıcı seçin!")
            return
        
        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.service_status_label.config(text="▶️ Servis: Çalışıyor")
        
        self.log_message("🚀 Fabrika yazıcı sistemi başlatıldı")
        self.log_message(f"🖨️ Aktif yazıcı: {self.printer_manager.selected_printer}")
        self.log_message(f"⚡ Kontrol hızı: Her {self.check_interval} saniyede bir")
        
        # Arka plan servisi başlat
        self.service_thread = threading.Thread(target=self.service_loop, daemon=True)
        self.service_thread.start()
    
    def servisi_durdur(self):
        """Ana servisi durdur"""
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.service_status_label.config(text="⏸️ Servis: Durduruldu")
        
        self.log_message("⏹️ Fabrika yazıcı sistemi durduruldu")
    
    def service_loop(self):
        """Ana servis döngüsü"""
        while self.is_running:
            try:
                self.yeni_siparisleri_kontrol_et()
                time.sleep(self.check_interval)
            except Exception as e:
                self.root.after(0, lambda: self.log_message(f"❌ Servis hatası: {str(e)}"))
                time.sleep(5)
    
    def yeni_siparisleri_kontrol_et(self):
        """Yeni siparişleri kontrol et ve işle"""
        try:
            url = f"{self.api_url}/orders/api/factory/orders/"
            params = {'token': self.token, 'days': 7}  # Son 7 günün siparişlerini getir
            
            if self.last_check_time:
                params['last_check'] = self.last_check_time.isoformat()
            
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                orders = data.get('orders', [])
                
                self.root.after(0, lambda: self.connection_label.config(text="🟢 Bağlantı: Aktif"))
                self.root.after(0, lambda: self.yeni_siparisleri_isle(orders))
                
                self.last_check_time = datetime.now(timezone.utc)
                self.root.after(0, lambda: self.last_check_label.config(
                    text=f"Son Kontrol: {self.last_check_time.strftime('%H:%M:%S')}"
                ))
                
            else:
                self.root.after(0, lambda: self.connection_label.config(text="🔴 Bağlantı: API Hatası"))
                
        except Exception as e:
            self.root.after(0, lambda: self.connection_label.config(text="🔴 Bağlantı: Hata"))
    
    def yeni_siparisleri_isle(self, orders):
        """Yeni siparişleri işle"""
        new_orders = [order for order in orders if order['id'] not in self.processed_orders]
        
        if new_orders:
            self.log_message(f"🆕 {len(new_orders)} yeni sipariş alındı")
            
            for order in new_orders:
                self.siparis_yazdir(order)
                self.processed_orders.add(order['id'])
        
        # Tüm siparişleri güncelle
        self.siparisleri_guncelle(orders)
    
    def siparis_yazdir(self, order):
        """Siparişi gerçekten yazdır"""
        try:
            self.log_message(f"🖨️ Yazdırılıyor: {order['order_number']} - {order['branch_name']}")
            
            # Sipariş formatını hazırla
            formatted_text = self.siparis_formatla(order)
            
            # Konsola yazdır (test için)
            print("\n" + "="*60)
            print("YAZICI ÇIKTISI:")
            print(formatted_text)
            print("="*60)
            
            # Yazıcıdan yazdır
            success = self.printer_manager.metin_yazdir(formatted_text)
            
            if success:
                # API'ye yazdırıldığını bildir
                self.siparis_yazdirildi_api(order['id'])
                self.log_message(f"✅ Başarıyla yazdırıldı: {order['order_number']}")
            else:
                self.log_message(f"❌ Yazdırma başarısız: {order['order_number']}")
            
        except Exception as e:
            self.log_message(f"❌ Yazdırma hatası: {str(e)}")
    
    def siparis_formatla(self, order):
        """Siparişi üretim odaklı yazdırma formatına dönüştür"""
        lines = []
        lines.append("=" * 50)
        lines.append("      TATO PASTA & BAKLAVA")
        lines.append("        ÜRETİM SİPARİŞİ")
        lines.append("=" * 50)
        lines.append("")
        
        lines.append(f"Sipariş No    : {order['order_number']}")
        lines.append(f"Şube          : {order['branch_name']}")
        lines.append(f"Teslimat      : {self.format_date(order['delivery_date'])}")
        lines.append(f"Sipariş Zamanı: {self.format_datetime(order['created_at'])}")
        lines.append(f"Sipariş Veren : {order['created_by']}")
        
        if order.get('notes'):
            lines.append(f"Özel Notlar   : {order['notes']}")
        
        lines.append("")
        lines.append("=" * 50)
        lines.append("             ÜRETİM LİSTESİ")
        lines.append("=" * 50)
        
        total_items = 0
        for item in order['items']:
            # Sadece ürün adı ve miktarı göster
            product_line = f"{item['product_name']:<35} {item['quantity']:>6.0f} {item['unit']}"
            lines.append(product_line)
            
            if item.get('notes'):
                lines.append(f"  → Not: {item['notes']}")
            
            total_items += item['quantity']
        
        lines.append("=" * 50)
        lines.append(f"TOPLAM ÜRÜN ADETİ: {total_items:>6.0f}")
        lines.append("")
        lines.append("⚠️  ÜRETİM TALİMATLARI:")
        lines.append("   • Hijyen kurallarına uyunuz")
        lines.append("   • Teslimat tarihine dikkat ediniz")
        lines.append("   • Kalite kontrolü yapınız")
        lines.append("")
        
        # Yazıcı ve yazdırma bilgisi
        lines.append("-" * 50)
        lines.append(f"Yazdırma: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
        lines.append(f"Yazıcı  : {self.printer_manager.selected_printer}")
        lines.append("=" * 50)
        lines.append("")
        
        return "\n".join(lines)
    
    def siparis_yazdirildi_api(self, order_id):
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
    
    # Test metodları - gerçek çalışan
    def hizli_test(self):
        """Hızlı test yazdırma"""
        if not self.printer_manager.selected_printer:
            messagebox.showwarning("Uyarı", "Önce bir yazıcı seçin")
            return
        
        self.test_results.insert(tk.END, "⚡ HIZLI TEST BAŞLATILIYOR...\n")
        self.test_results.see(tk.END)
        
        def test():
            success = self.printer_manager.yazici_test_et(self.printer_manager.selected_printer)
            result = "✅ BAŞARILI" if success else "❌ BAŞARISIZ"
            self.root.after(0, lambda: self.test_results.insert(tk.END, f"⚡ Hızlı test sonucu: {result}\n"))
            self.root.after(0, lambda: self.test_results.see(tk.END))
        
        threading.Thread(target=test, daemon=True).start()
    
    def metin_test(self):
        """Metin test yazdırma"""
        if not self.printer_manager.selected_printer:
            messagebox.showwarning("Uyarı", "Önce bir yazıcı seçin")
            return
        
        self.test_results.insert(tk.END, "📄 METİN TESTİ BAŞLATILIYOR...\n")
        self.test_results.see(tk.END)
        
        test_text = f"""
===============================================
      TATO PASTA & BAKLAVA
    ÜRETİM SİSTEMİ TEST ÇIKTISI
===============================================

Tarih: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
Yazıcı: {self.printer_manager.selected_printer}

Bu bir üretim sistemi test yazdırmasıdır.

KARAKTER TESTİ:
• Türkçe: ÇĞİÖŞÜ çğıöşü
• Sayılar: 0123456789
• Özel: →·⚠️✅⏳📦

ÜRETİM TEST LİSTESİ:
Baklava Çeşitleri        25 adet
Pasta Çeşitleri          15 adet
Kurabiye                 50 adet
                      --------
TOPLAM                   90 adet

⚠️ Test başarılıysa tüm karakterler
   düzgün görünmelidir.

TATO PASTA & BAKLAVA
Üretim Sistemi - Test Modu
===============================================
"""
        
        def test():
            success = self.printer_manager.metin_yazdir(test_text)
            result = "✅ BAŞARILI" if success else "❌ BAŞARISIZ"
            self.root.after(0, lambda: self.test_results.insert(tk.END, f"📄 Metin test sonucu: {result}\n"))
            self.root.after(0, lambda: self.test_results.see(tk.END))
        
        threading.Thread(target=test, daemon=True).start()
    
    def yazici_durumu_goster(self):
        """Yazıcı durumu bilgisi göster"""
        if not self.printer_manager.selected_printer:
            messagebox.showwarning("Uyarı", "Önce bir yazıcı seçin")
            return
        
        self.test_results.insert(tk.END, "🖨️ YAZICI DURUMU SORGULANIYOR...\n")
        
        printer_info = self.printer_manager.available_printers.get(self.printer_manager.selected_printer, {})
        
        self.test_results.insert(tk.END, f"📌 Yazıcı Adı: {printer_info.get('name', 'Bilinmiyor')}\n")
        self.test_results.insert(tk.END, f"📊 Durum: {printer_info.get('status', 'Bilinmiyor')}\n")
        self.test_results.insert(tk.END, f"🔌 Port: {printer_info.get('port', 'Bilinmiyor')}\n")
        self.test_results.insert(tk.END, f"💿 Sürücü: {printer_info.get('driver', 'Bilinmiyor')}\n")
        self.test_results.insert(tk.END, f"📍 Konum: {printer_info.get('location', 'Bilinmiyor')}\n")
        self.test_results.insert(tk.END, f"✅ Varsayılan: {'Evet' if printer_info.get('is_default', False) else 'Hayır'}\n")
        self.test_results.insert(tk.END, "-" * 40 + "\n")
        self.test_results.see(tk.END)
    
    def ag_test(self):
        """Ağ bağlantı testi"""
        self.test_results.insert(tk.END, "🌐 AĞ BAĞLANTISI TESTİ...\n")
        
        def test():
            # İnternet testi
            try:
                response = requests.get("https://www.google.com", timeout=5)
                if response.status_code == 200:
                    self.root.after(0, lambda: self.test_results.insert(tk.END, "✅ İnternet bağlantısı: BAŞARILI\n"))
                else:
                    self.root.after(0, lambda: self.test_results.insert(tk.END, "❌ İnternet bağlantısı: BAŞARISIZ\n"))
            except:
                self.root.after(0, lambda: self.test_results.insert(tk.END, "❌ İnternet bağlantısı: BAŞARISIZ\n"))
            
            # API testi
            try:
                url = f"{self.api_url}/orders/api/factory/orders/"
                params = {'token': self.token, 'days': 7}
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    self.root.after(0, lambda: self.test_results.insert(tk.END, "✅ API bağlantısı: BAŞARILI\n"))
                else:
                    self.root.after(0, lambda: self.test_results.insert(tk.END, f"❌ API bağlantısı: BAŞARISIZ (HTTP {response.status_code})\n"))
            except Exception as e:
                self.root.after(0, lambda: self.test_results.insert(tk.END, f"❌ API bağlantısı: BAŞARISIZ ({str(e)[:30]})\n"))
            
            self.root.after(0, lambda: self.test_results.insert(tk.END, "-" * 40 + "\n"))
            self.root.after(0, lambda: self.test_results.see(tk.END))
        
        threading.Thread(target=test, daemon=True).start()
    
    def ozel_metin_yazdir(self):
        """Özel metin yazdır"""
        if not self.printer_manager.selected_printer:
            messagebox.showwarning("Uyarı", "Önce bir yazıcı seçin")
            return
        
        custom_text = self.custom_text.get('1.0', tk.END).strip()
        if not custom_text:
            messagebox.showwarning("Uyarı", "Test metni boş olamaz")
            return
        
        self.test_results.insert(tk.END, "✏️ ÖZEL METİN YAZDIRILIYOR...\n")
        self.test_results.see(tk.END)
        
        def test():
            success = self.printer_manager.metin_yazdir(custom_text)
            result = "✅ BAŞARILI" if success else "❌ BAŞARISIZ"
            self.root.after(0, lambda: self.test_results.insert(tk.END, f"✏️ Özel metin sonucu: {result}\n"))
            self.root.after(0, lambda: self.test_results.see(tk.END))
        
        threading.Thread(target=test, daemon=True).start()
    
    # Diğer metodlar
    def manuel_yenile(self):
        """Manuel yenileme"""
        self.yazicilari_tara()
        self.baglanti_test_et()
    
    def ayarlari_kaydet(self):
        """Ayarları kaydet"""
        self.api_url = self.url_entry.get()
        self.token = self.token_entry.get()
        
        try:
            self.check_interval = int(self.interval_entry.get())
        except:
            self.check_interval = 30
        
        self.log_message("⚙️ Ayarlar kaydedildi")
        messagebox.showinfo("Ayarlar", "Ayarlar başarıyla kaydedildi!")
    
    def loglari_yenile(self):
        """Logları yenile"""
        self.log_message("🔄 Loglar yenilendi")
    
    def loglari_temizle(self):
        """Logları temizle"""
        self.log_text.delete('1.0', tk.END)
        self.log_message("🗑️ Log alanı temizlendi")
    
    def loglari_kaydet(self):
        """Logları dosyaya kaydet"""
        try:
            log_content = self.log_text.get('1.0', tk.END)
            filename = f"log_yedek_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(log_content)
            
            self.log_message(f"💾 Loglar kaydedildi: {filename}")
            messagebox.showinfo("Kaydet", f"Loglar başarıyla kaydedildi:\n{filename}")
        except Exception as e:
            messagebox.showerror("Hata", f"Log kaydetme hatası:\n{str(e)}")
    
    def format_date(self, date_str):
        """Tarih formatla"""
        try:
            date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return date.strftime('%d.%m.%Y')
        except:
            return date_str
    
    def format_datetime(self, datetime_str):
        """Tarih-saat formatla"""
        try:
            dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
            return dt.strftime('%d.%m.%Y %H:%M')
        except:
            return datetime_str
    
    def log_message(self, message):
        """Log mesajı ekle"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        # GUI'ye ekle
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        
        # Durum çubuğunu güncelle
        self.status_bar.config(text=message)
        
        # Dosyaya kaydet
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{datetime.now().isoformat()}] {message}\n")
        except:
            pass
    
    def on_closing(self):
        """Program kapanış"""
        if self.is_running:
            self.servisi_durdur()
        
        self.log_message("👋 ÇALIŞAN Fabrika Yazıcı Programı kapatılıyor...")
        self.root.destroy()
    
    def run(self):
        """Programı çalıştır"""
        self.root.mainloop()


def main():
    """Ana fonksiyon"""
    try:
        app = CalisanFabrikaYaziciProgram()
        app.run()
    except Exception as e:
        messagebox.showerror("Hata", f"Program başlatılamadı: {str(e)}")


if __name__ == "__main__":
    main()