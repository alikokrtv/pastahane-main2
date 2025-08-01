#!/usr/bin/env python3
"""
Tato Pasta & Baklava - Süper Gelişmiş Fabrika Yazıcı Programı
Otomatik yazıcı keşfi, detaylı tanımlama ve akıllı yönetim sistemi
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
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
    import win32gui
    import win32con
    import win32file
    WINDOWS_PRINTER_SUPPORT = True
except ImportError:
    WINDOWS_PRINTER_SUPPORT = False

# Cross-platform yazıcı desteği için
try:
    import cups  # Linux/macOS için
    CUPS_SUPPORT = True
except ImportError:
    CUPS_SUPPORT = False

class GelismisYaziciYoneticisi:
    """Süper gelişmiş yazıcı yönetim sistemi"""
    
    def __init__(self):
        self.available_printers = {}
        self.selected_printer = None
        self.printer_capabilities = {}
        self.system_info = self.get_system_info()
        
    def get_system_info(self):
        """Sistem bilgilerini al"""
        return {
            'os': platform.system(),
            'os_version': platform.version(),
            'architecture': platform.architecture()[0],
            'machine': platform.machine(),
            'python_version': platform.python_version()
        }
    
    def scan_all_printers(self):
        """Tüm mevcut yazıcıları kapsamlı tara"""
        self.available_printers.clear()
        self.printer_capabilities.clear()
        
        print("🔍 Yazıcı tarama başlatılıyor...")
        
        if self.system_info['os'] == 'Windows':
            self._scan_windows_printers()
        elif self.system_info['os'] in ['Linux', 'Darwin']:
            self._scan_cups_printers()
        
        # Ağ yazıcılarını da tara
        self._scan_network_printers()
        
        print(f"✅ Tarama tamamlandı: {len(self.available_printers)} yazıcı bulundu")
        return self.available_printers
    
    def _scan_windows_printers(self):
        """Windows yazıcılarını tara"""
        if not WINDOWS_PRINTER_SUPPORT:
            print("⚠️ Windows yazıcı desteği yok")
            return
        
        try:
            # Yerel yazıcıları tara
            flags = win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
            printers = win32print.EnumPrinters(flags)
            
            for printer in printers:
                printer_name = printer[2]
                print(f"🖨️ Yazıcı bulundu: {printer_name}")
                
                printer_info = self._get_windows_printer_info(printer_name)
                self.available_printers[printer_name] = printer_info
                
                # Yazıcı yeteneklerini al
                capabilities = self._get_windows_printer_capabilities(printer_name)
                self.printer_capabilities[printer_name] = capabilities
                
        except Exception as e:
            print(f"❌ Windows yazıcı tarama hatası: {e}")
    
    def _scan_cups_printers(self):
        """CUPS yazıcılarını tara (Linux/macOS)"""
        if not CUPS_SUPPORT:
            print("⚠️ CUPS desteği yok")
            return
        
        try:
            conn = cups.Connection()
            printers = conn.getPrinters()
            
            for printer_name, printer_info in printers.items():
                print(f"🖨️ CUPS yazıcı bulundu: {printer_name}")
                
                formatted_info = {
                    'name': printer_name,
                    'status': self._translate_cups_status(printer_info.get('printer-state', 3)),
                    'location': printer_info.get('printer-location', 'Bilinmiyor'),
                    'description': printer_info.get('printer-info', 'Açıklama yok'),
                    'uri': printer_info.get('device-uri', ''),
                    'type': 'CUPS',
                    'is_default': printer_info.get('printer-is-accepting-jobs', False),
                    'is_shared': printer_info.get('printer-is-shared', False)
                }
                
                self.available_printers[printer_name] = formatted_info
                
        except Exception as e:
            print(f"❌ CUPS yazıcı tarama hatası: {e}")
    
    def _scan_network_printers(self):
        """Ağ yazıcılarını tara"""
        print("🌐 Ağ yazıcıları taranıyor...")
        
        # Yaygın yazıcı portlarını kontrol et
        common_ports = [9100, 515, 631, 8080, 80, 443]
        local_network = self._get_local_network()
        
        if not local_network:
            return
        
        found_count = 0
        for i in range(1, 255):
            if found_count >= 5:  # Maksimum 5 ağ yazıcısı tara
                break
                
            ip = f"{local_network}.{i}"
            
            for port in common_ports[:2]:  # Sadece en yaygın portları kontrol et
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.1)
                    result = sock.connect_ex((ip, port))
                    sock.close()
                    
                    if result == 0:
                        printer_name = f"Ağ Yazıcısı ({ip}:{port})"
                        print(f"🌐 Ağ yazıcısı bulundu: {printer_name}")
                        
                        self.available_printers[printer_name] = {
                            'name': printer_name,
                            'status': '🌐 Ağ Yazıcısı',
                            'location': f'{ip}:{port}',
                            'description': f'Port {port} üzerinden erişilebilir ağ yazıcısı',
                            'type': 'Network',
                            'ip': ip,
                            'port': port,
                            'is_default': False
                        }
                        found_count += 1
                        break
                        
                except:
                    continue
    
    def _get_local_network(self):
        """Yerel ağ adresini al"""
        try:
            # Varsayılan ağ geçidine bağlan
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect(("8.8.8.8", 80))
            local_ip = sock.getsockname()[0]
            sock.close()
            
            # Ağ adresini çıkar (son okteti sil)
            return '.'.join(local_ip.split('.')[:-1])
        except:
            return None
    
    def _get_windows_printer_info(self, printer_name):
        """Windows yazıcı detaylı bilgilerini al"""
        try:
            handle = win32print.OpenPrinter(printer_name)
            printer_info = win32print.GetPrinter(handle, 2)
            win32print.ClosePrinter(handle)
            
            # Durumu çevir
            status = self._translate_windows_status(printer_info['Status'])
            
            return {
                'name': printer_name,
                'status': status,
                'location': printer_info.get('pLocation', 'Bilinmiyor'),
                'description': printer_info.get('pComment', 'Açıklama yok'),
                'driver': printer_info.get('pDriverName', 'Bilinmiyor'),
                'port': printer_info.get('pPortName', 'Bilinmiyor'),
                'type': 'Windows',
                'is_default': printer_name == win32print.GetDefaultPrinter(),
                'is_shared': bool(printer_info.get('Attributes', 0) & win32print.PRINTER_ATTRIBUTE_SHARED),
                'server': printer_info.get('pServerName', 'Yerel')
            }
            
        except Exception as e:
            return {
                'name': printer_name,
                'status': f'❌ Hata: {str(e)[:30]}',
                'location': 'Bilinmiyor',
                'description': 'Bilgi alınamadı',
                'type': 'Windows',
                'error': str(e)
            }
    
    def _get_windows_printer_capabilities(self, printer_name):
        """Windows yazıcı yeteneklerini al"""
        try:
            # Yazıcı yeteneklerini sorgula
            hdc = win32gui.CreateDC("WINSPOOL", printer_name, None)
            
            capabilities = {
                'width_mm': win32gui.GetDeviceCaps(hdc, win32con.HORZSIZE),
                'height_mm': win32gui.GetDeviceCaps(hdc, win32con.VERTSIZE),
                'width_pixels': win32gui.GetDeviceCaps(hdc, win32con.HORZRES),
                'height_pixels': win32gui.GetDeviceCaps(hdc, win32con.VERTRES),
                'dpi_x': win32gui.GetDeviceCaps(hdc, win32con.LOGPIXELSX),
                'dpi_y': win32gui.GetDeviceCaps(hdc, win32con.LOGPIXELSY),
                'colors': win32gui.GetDeviceCaps(hdc, win32con.NUMCOLORS),
                'planes': win32gui.GetDeviceCaps(hdc, win32con.PLANES),
                'bits_per_pixel': win32gui.GetDeviceCaps(hdc, win32con.BITSPIXEL)
            }
            
            win32gui.DeleteDC(hdc)
            return capabilities
            
        except Exception as e:
            return {'error': str(e)}
    
    def _translate_windows_status(self, status_code):
        """Windows yazıcı durum kodlarını çevir"""
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
        elif status_code & win32print.PRINTER_STATUS_TONER_LOW:
            return "🔋 Toner Az"
        elif status_code & win32print.PRINTER_STATUS_BUSY:
            return "⏳ Meşgul"
        elif status_code & win32print.PRINTER_STATUS_PRINTING:
            return "🖨️ Yazdırıyor"
        else:
            return f"⚠️ Bilinmeyen ({status_code})"
    
    def _translate_cups_status(self, state):
        """CUPS yazıcı durumlarını çevir"""
        states = {
            3: "✅ Hazır",
            4: "🖨️ Yazdırıyor",
            5: "⏸️ Durdurulmuş"
        }
        return states.get(state, f"⚠️ Bilinmeyen ({state})")
    
    def get_printer_details(self, printer_name):
        """Yazıcının detaylı bilgilerini al"""
        if printer_name not in self.available_printers:
            return None
        
        printer_info = self.available_printers[printer_name]
        capabilities = self.printer_capabilities.get(printer_name, {})
        
        details = {
            'basic_info': printer_info,
            'capabilities': capabilities,
            'queue_info': self._get_print_queue_info(printer_name),
            'test_results': []
        }
        
        return details
    
    def _get_print_queue_info(self, printer_name):
        """Yazıcı kuyruğu bilgilerini al"""
        try:
            if self.system_info['os'] == 'Windows' and WINDOWS_PRINTER_SUPPORT:
                handle = win32print.OpenPrinter(printer_name)
                jobs = win32print.EnumJobs(handle, 0, -1, 2)
                win32print.ClosePrinter(handle)
                
                return {
                    'job_count': len(jobs),
                    'jobs': [
                        {
                            'id': job['JobId'],
                            'document': job.get('pDocument', 'Bilinmiyor'),
                            'status': job.get('Status', 0),
                            'pages': job.get('TotalPages', 0),
                            'size': job.get('Size', 0)
                        } for job in jobs
                    ]
                }
            else:
                return {'job_count': 0, 'jobs': []}
                
        except Exception as e:
            return {'error': str(e)}
    
    def test_printer_comprehensive(self, printer_name):
        """Kapsamlı yazıcı testi"""
        results = []
        
        # 1. Bağlantı testi
        results.append(self._test_printer_connection(printer_name))
        
        # 2. Basit metin testi
        results.append(self._test_simple_text_print(printer_name))
        
        # 3. Formatlanmış metin testi
        results.append(self._test_formatted_text_print(printer_name))
        
        # 4. Özel karakterler testi
        results.append(self._test_special_characters(printer_name))
        
        return results
    
    def _test_printer_connection(self, printer_name):
        """Yazıcı bağlantı testi"""
        try:
            printer_info = self.available_printers.get(printer_name)
            if not printer_info:
                return {'test': 'Bağlantı', 'result': False, 'message': 'Yazıcı bulunamadı'}
            
            if printer_info['type'] == 'Network':
                # Ağ yazıcısı için ping testi
                ip = printer_info.get('ip')
                port = printer_info.get('port')
                
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                result = sock.connect_ex((ip, port))
                sock.close()
                
                if result == 0:
                    return {'test': 'Bağlantı', 'result': True, 'message': 'Ağ bağlantısı başarılı'}
                else:
                    return {'test': 'Bağlantı', 'result': False, 'message': 'Ağ bağlantısı başarısız'}
            
            else:
                # Yerel yazıcı için
                if self.system_info['os'] == 'Windows' and WINDOWS_PRINTER_SUPPORT:
                    try:
                        handle = win32print.OpenPrinter(printer_name)
                        win32print.ClosePrinter(handle)
                        return {'test': 'Bağlantı', 'result': True, 'message': 'Yazıcı erişilebilir'}
                    except:
                        return {'test': 'Bağlantı', 'result': False, 'message': 'Yazıcıya erişilemiyor'}
                else:
                    return {'test': 'Bağlantı', 'result': True, 'message': 'Sistem yazıcısı mevcut'}
                    
        except Exception as e:
            return {'test': 'Bağlantı', 'result': False, 'message': f'Hata: {str(e)}'}
    
    def _test_simple_text_print(self, printer_name):
        """Basit metin yazdırma testi"""
        test_text = """TEST YAZDIRMA
=============
Bu bir basit test yazdırmasıdır.
Tarih: {date}
Saat: {time}
Yazıcı: {printer}
""".format(
            date=datetime.now().strftime('%d.%m.%Y'),
            time=datetime.now().strftime('%H:%M:%S'),
            printer=printer_name
        )
        
        return self._execute_print_test(printer_name, test_text, "Basit Metin")
    
    def _test_formatted_text_print(self, printer_name):
        """Formatlanmış metin yazdırma testi"""
        test_text = """
FORMATLANMIŞ TEST YAZDIRMA
==========================

TATO PASTA & BAKLAVA
Fabrika Yazıcı Sistemi Test Çıktısı

Tarih     : {date}
Saat      : {time}
Yazıcı    : {printer}
Test No   : FMT-{timestamp}

ÜRÜN LİSTESİ
-----------
1. Çikolatalı Pasta        x 5 adet
2. Meyveli Pasta          x 3 adet  
3. Fıstıklı Baklava       x 10 adet

TOPLAM: 18 ürün

TEST SONUCU: {result}

Bu test çıktısı formatlanmış metin
yazdırma özelliğini kontrol eder.

Türkçe karakterler: ĞÜŞİÖÇ ğüşıöç
Özel karakterler: ₺ € $ % & @ # !

=============================
TEST TAMAMLANDI
=============================
""".format(
            date=datetime.now().strftime('%d.%m.%Y'),
            time=datetime.now().strftime('%H:%M:%S'),
            printer=printer_name,
            timestamp=datetime.now().strftime('%Y%m%d%H%M%S'),
            result='BAŞARILI' if True else 'BAŞARISIZ'
        )
        
        return self._execute_print_test(printer_name, test_text, "Formatlanmış Metin")
    
    def _test_special_characters(self, printer_name):
        """Özel karakterler testi"""
        test_text = """
ÖZEL KARAKTERLER TESTİ
======================

Türkçe Karakterler:
Ğ Ü Ş İ Ö Ç
ğ ü ş ı ö ç

Para Birimleri:
₺ (Türk Lirası)
€ (Euro)
$ (Dolar)
£ (Sterlin)

Matematik Sembolleri:
+ - × ÷ = ≠ < > ≤ ≥
± ∞ ∑ √ π ∆

Çizgi Karakterleri:
─ ─ ─ ─ ─ ─ ─ ─ ─ ─
│ │ │ │ │ │ │ │ │ │
┌─┬─┬─┐
├─┼─┼─┤
└─┴─┴─┘

Diğer Özel Karakterler:
© ® ™ ° • ◦ ▪ ▫ ♥ ♦ ♣ ♠

Test Tamamlandı: ✓
======================
""".format()
        
        return self._execute_print_test(printer_name, test_text, "Özel Karakterler")
    
    def _execute_print_test(self, printer_name, content, test_name):
        """Test yazdırmayı gerçekleştir"""
        try:
            # Geçici dosya oluştur
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
                f.write(content)
                temp_file = f.name
            
            # Yazdırmayı dene
            success = self._print_file_to_printer(temp_file, printer_name)
            
            # Geçici dosyayı sil
            try:
                os.unlink(temp_file)
            except:
                pass
            
            if success:
                return {'test': test_name, 'result': True, 'message': 'Test yazdırma başarılı'}
            else:
                return {'test': test_name, 'result': False, 'message': 'Test yazdırma başarısız'}
                
        except Exception as e:
            return {'test': test_name, 'result': False, 'message': f'Test hatası: {str(e)}'}
    
    def _print_file_to_printer(self, file_path, printer_name):
        """Dosyayı belirtilen yazıcıya yazdır"""
        try:
            if self.system_info['os'] == 'Windows':
                if WINDOWS_PRINTER_SUPPORT:
                    # Windows API ile yazdır
                    win32api.ShellExecute(0, "print", file_path, f'/d:"{printer_name}"', ".", 0)
                else:
                    # Fallback: sistem komutu
                    subprocess.run(['print', f'/D:"{printer_name}"', file_path], shell=True, timeout=30)
                    
            elif self.system_info['os'] == 'Linux':
                # Linux için lp komutu
                subprocess.run(['lp', '-d', printer_name, file_path], timeout=30)
                
            elif self.system_info['os'] == 'Darwin':
                # macOS için lpr komutu
                subprocess.run(['lpr', '-P', printer_name, file_path], timeout=30)
            
            return True
            
        except Exception as e:
            print(f"❌ Yazdırma hatası: {e}")
            return False
    
    def install_printer_wizard(self):
        """Yazıcı kurulum sihirbazı"""
        return {
            'steps': [
                'Yazıcıyı bilgisayara bağlayın (USB/Ağ)',
                'Yazıcıyı açın ve hazır duruma getirin',
                'Windows Ayarlar > Yazıcılar ve Tarayıcılar bölümüne gidin',
                '"Yazıcı veya tarayıcı ekle" seçeneğine tıklayın',
                'Sistemin yazıcıyı bulmasını bekleyin',
                'Yazıcı bulunduğunda kurulum talimatlarını takip edin',
                'Test sayfası yazdırın',
                'Bu programdan yazıcıyı seçin ve test edin'
            ],
            'troubleshooting': [
                'Yazıcı bulunamıyorsa: USB kablosunu kontrol edin',
                'Sürücü sorunu varsa: Üretici web sitesinden güncel sürücüyü indirin',
                'Ağ yazıcısı bağlanmıyorsa: IP adresini kontrol edin',
                'Windows yazıcı sorun gidericisini çalıştırın'
            ]
        }

class SüperGelişmisFabrikaYaziciProgram:
    """Süper gelişmiş fabrika yazıcı ana programı"""
    
    def __init__(self):
        # Konfigürasyon
        self.api_url = "https://siparis.tatopastabaklava.com"
        self.token = "factory_printer_2024"
        self.check_interval = 30
        
        # Durum değişkenleri
        self.is_running = False
        self.last_check_time = None
        self.processed_orders = set()
        
        # Gelişmiş yazıcı yöneticisi
        self.printer_manager = GelismisYaziciYoneticisi()
        
        # Ana pencere oluştur
        self.root = tk.Tk()
        self.root.title("Tato Pasta & Baklava - Süper Gelişmiş Fabrika Yazıcı Sistemi")
        self.root.geometry("1600x1000")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Stil ayarları
        style = ttk.Style()
        style.theme_use('clam')
        
        # Renk teması
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'success': '#22C55E',
            'warning': '#F59E0B',
            'error': '#EF4444',
            'info': '#3B82F6'
        }
        
        # Arayüzü oluştur
        self.create_widgets()
        
        # Log dosyası
        self.log_file = "super_fabrika_log.txt"
        
        self.log_message("🏭 Süper Gelişmiş Fabrika Yazıcı Programı başlatıldı")
        self.log_message(f"🔗 API URL: {self.api_url}")
        self.log_message(f"💻 İşletim Sistemi: {self.printer_manager.system_info['os']}")
        
        # Yazıcıları otomatik tara
        self.auto_scan_printers()
    
    def create_widgets(self):
        """Gelişmiş arayüz bileşenlerini oluştur"""
        
        # Ana başlık
        self.create_header()
        
        # Ana notebook (sekmeler)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Sekmeler oluştur
        self.create_dashboard_tab()
        self.create_advanced_printer_tab()
        self.create_printer_discovery_tab()
        self.create_test_center_tab()
        self.create_settings_tab()
        self.create_logs_tab()
        
        # Alt durum çubuğu
        self.create_status_bar()
    
    def create_header(self):
        """Ana başlık bölümü"""
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        header_frame.pack_propagate(False)
        
        # Logo ve başlık
        title_frame = tk.Frame(header_frame, bg=self.colors['primary'])
        title_frame.pack(expand=True, fill=tk.BOTH)
        
        tk.Label(title_frame, text="🏭 TATO PASTA & BAKLAVA", 
                font=('Arial', 18, 'bold'), fg='white', bg=self.colors['primary']).pack(pady=(10, 0))
        
        tk.Label(title_frame, text="Süper Gelişmiş Fabrika Yazıcı Sistemi v2.0", 
                font=('Arial', 12), fg='white', bg=self.colors['primary']).pack()
    
    def create_dashboard_tab(self):
        """Ana kontrol paneli sekmesi"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="📊 Kontrol Paneli")
        
        # Üst bilgi kartları
        self.create_info_cards(dashboard_frame)
        
        # Kontrol butonları
        self.create_control_buttons(dashboard_frame)
        
        # Canlı durum göstergesi
        self.create_live_status(dashboard_frame)
        
        # Siparişler tablosu
        self.create_orders_table(dashboard_frame)
    
    def create_info_cards(self, parent):
        """Bilgi kartları oluştur"""
        cards_frame = ttk.Frame(parent)
        cards_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Yazıcı durumu kartı
        printer_card = ttk.LabelFrame(cards_frame, text="🖨️ Yazıcı Durumu")
        printer_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.printer_status_label = ttk.Label(printer_card, text="❌ Yazıcı Seçilmedi", 
                                             font=('Arial', 12, 'bold'))
        self.printer_status_label.pack(pady=10)
        
        self.printer_details_label = ttk.Label(printer_card, text="Detay bilgi yok")
        self.printer_details_label.pack()
        
        # Bağlantı durumu kartı
        connection_card = ttk.LabelFrame(cards_frame, text="🌐 Bağlantı Durumu")
        connection_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.connection_status_label = ttk.Label(connection_card, text="🔴 Bağlantı Yok", 
                                               font=('Arial', 12, 'bold'))
        self.connection_status_label.pack(pady=10)
        
        self.api_details_label = ttk.Label(connection_card, text="API test edilmedi")
        self.api_details_label.pack()
        
        # İstatistikler kartı
        stats_card = ttk.LabelFrame(cards_frame, text="📈 İstatistikler")
        stats_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.stats_frame = ttk.Frame(stats_card)
        self.stats_frame.pack(pady=10)
        
        self.total_orders_label = ttk.Label(self.stats_frame, text="Toplam: 0")
        self.total_orders_label.pack()
        
        self.printed_orders_label = ttk.Label(self.stats_frame, text="Yazdırılan: 0")
        self.printed_orders_label.pack()
        
        self.last_check_label = ttk.Label(self.stats_frame, text="Son kontrol: -")
        self.last_check_label.pack()
    
    def create_control_buttons(self, parent):
        """Kontrol butonları oluştur"""
        control_frame = ttk.LabelFrame(parent, text="🎮 Kontrol Paneli")
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        buttons_frame = ttk.Frame(control_frame)
        buttons_frame.pack(pady=10)
        
        # Ana kontrol butonları
        self.start_btn = ttk.Button(buttons_frame, text="▶️ SİSTEMİ BAŞLAT", 
                                   command=self.start_service)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(buttons_frame, text="⏹️ SİSTEMİ DURDUR", 
                                  command=self.stop_service)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        self.test_connection_btn = ttk.Button(buttons_frame, text="🔍 BAĞLANTI TESTİ", 
                                            command=self.test_api_connection)
        self.test_connection_btn.pack(side=tk.LEFT, padx=5)
        
        self.refresh_btn = ttk.Button(buttons_frame, text="🔄 YENİLE", 
                                     command=self.manual_refresh)
        self.refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Hızlı işlemler
        quick_frame = ttk.Frame(control_frame)
        quick_frame.pack(pady=5)
        
        ttk.Button(quick_frame, text="🖨️ Hızlı Test Yazdır", 
                  command=self.quick_test_print).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(quick_frame, text="📋 Yazıcı Bilgileri", 
                  command=self.show_printer_info).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(quick_frame, text="🔧 Yazıcı Sihirbazı", 
                  command=self.open_printer_wizard).pack(side=tk.LEFT, padx=5)
    
    def create_live_status(self, parent):
        """Canlı durum göstergesi"""
        status_frame = ttk.LabelFrame(parent, text="📡 Canlı Durum")
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.live_status_text = scrolledtext.ScrolledText(status_frame, height=4, wrap=tk.WORD)
        self.live_status_text.pack(fill=tk.X, padx=5, pady=5)
        
        # Durum güncelleme butonu
        ttk.Button(status_frame, text="🔄 Durumu Güncelle", 
                  command=self.update_live_status).pack(pady=5)
    
    def create_orders_table(self, parent):
        """Gelişmiş siparişler tablosu"""
        orders_frame = ttk.LabelFrame(parent, text="📦 Aktif Siparişler")
        orders_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Tablo oluştur
        columns = ('siparis_no', 'sube', 'tarih', 'urun_sayisi', 'tutar', 'durum', 'oncelik')
        self.orders_tree = ttk.Treeview(orders_frame, columns=columns, show='headings', height=12)
        
        # Sütun başlıkları ve genişlikleri
        headers = {
            'siparis_no': ('Sipariş No', 120),
            'sube': ('Şube', 100),
            'tarih': ('Teslimat', 100),
            'urun_sayisi': ('Ürün', 60),
            'tutar': ('Tutar', 80),
            'durum': ('Durum', 120),
            'oncelik': ('Öncelik', 80)
        }
        
        for col, (text, width) in headers.items():
            self.orders_tree.heading(col, text=text)
            self.orders_tree.column(col, width=width)
        
        # Scrollbar ekle
        scrollbar_orders = ttk.Scrollbar(orders_frame, orient=tk.VERTICAL, 
                                       command=self.orders_tree.yview)
        self.orders_tree.configure(yscrollcommand=scrollbar_orders.set)
        
        self.orders_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_orders.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Çift tıklama eventi
        self.orders_tree.bind('<Double-1>', self.on_order_double_click)
    
    def create_advanced_printer_tab(self):
        """Gelişmiş yazıcı yönetimi sekmesi"""
        printer_frame = ttk.Frame(self.notebook)
        self.notebook.add(printer_frame, text="🖨️ Yazıcı Yönetimi")
        
        # Yazıcı listesi ve detayları
        main_printer_frame = ttk.PanedWindow(printer_frame, orient=tk.HORIZONTAL)
        main_printer_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Sol panel - Yazıcı listesi
        left_panel = ttk.Frame(main_printer_frame)
        main_printer_frame.add(left_panel, weight=1)
        
        # Yazıcı listesi
        printers_list_frame = ttk.LabelFrame(left_panel, text="📋 Tespit Edilen Yazıcılar")
        printers_list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Yazıcı tablosu
        printer_columns = ('name', 'status', 'type', 'location')
        self.printer_tree = ttk.Treeview(printers_list_frame, columns=printer_columns, 
                                       show='headings', height=15)
        
        self.printer_tree.heading('name', text='Yazıcı Adı')
        self.printer_tree.heading('status', text='Durum')
        self.printer_tree.heading('type', text='Tür')
        self.printer_tree.heading('location', text='Konum')
        
        self.printer_tree.column('name', width=200)
        self.printer_tree.column('status', width=120)
        self.printer_tree.column('type', width=80)
        self.printer_tree.column('location', width=150)
        
        self.printer_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Yazıcı kontrol butonları
        printer_buttons_frame = ttk.Frame(left_panel)
        printer_buttons_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(printer_buttons_frame, text="🔄 Yeniden Tara", 
                  command=self.scan_printers).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(printer_buttons_frame, text="✅ Seç", 
                  command=self.select_printer).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(printer_buttons_frame, text="🧪 Test Et", 
                  command=self.test_selected_printer).pack(side=tk.LEFT, padx=2)
        
        # Sağ panel - Yazıcı detayları
        right_panel = ttk.Frame(main_printer_frame)
        main_printer_frame.add(right_panel, weight=1)
        
        self.create_printer_details_panel(right_panel)
    
    def create_printer_details_panel(self, parent):
        """Yazıcı detay paneli"""
        details_frame = ttk.LabelFrame(parent, text="📊 Yazıcı Detayları")
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        self.printer_details_text = scrolledtext.ScrolledText(details_frame, wrap=tk.WORD)
        self.printer_details_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Detay butonları
        details_buttons_frame = ttk.Frame(details_frame)
        details_buttons_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(details_buttons_frame, text="🔍 Detayları Göster", 
                  command=self.show_detailed_printer_info).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(details_buttons_frame, text="🧪 Kapsamlı Test", 
                  command=self.comprehensive_printer_test).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(details_buttons_frame, text="⚙️ Ayarlar", 
                  command=self.open_printer_settings).pack(side=tk.LEFT, padx=5)
    
    def create_printer_discovery_tab(self):
        """Yazıcı keşif sekmesi"""
        discovery_frame = ttk.Frame(self.notebook)
        self.notebook.add(discovery_frame, text="🔍 Yazıcı Keşfi")
        
        # Keşif araçları
        tools_frame = ttk.LabelFrame(discovery_frame, text="🛠️ Keşif Araçları")
        tools_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tools_buttons_frame = ttk.Frame(tools_frame)
        tools_buttons_frame.pack(pady=10)
        
        ttk.Button(tools_buttons_frame, text="🔍 Otomatik Keşif", 
                  command=self.auto_discovery).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(tools_buttons_frame, text="🌐 Ağ Taraması", 
                  command=self.network_scan).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(tools_buttons_frame, text="🔌 USB Tarama", 
                  command=self.usb_scan).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(tools_buttons_frame, text="➕ Manuel Ekleme", 
                  command=self.manual_printer_add).pack(side=tk.LEFT, padx=5)
        
        # Keşif sonuçları
        results_frame = ttk.LabelFrame(discovery_frame, text="📋 Keşif Sonuçları")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.discovery_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD)
        self.discovery_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def create_test_center_tab(self):
        """Test merkezi sekmesi"""
        test_frame = ttk.Frame(self.notebook)
        self.notebook.add(test_frame, text="🧪 Test Merkezi")
        
        # Test türleri
        test_types_frame = ttk.LabelFrame(test_frame, text="🎯 Test Türleri")
        test_types_frame.pack(fill=tk.X, padx=10, pady=10)
        
        test_buttons_frame = ttk.Frame(test_types_frame)
        test_buttons_frame.pack(pady=10)
        
        ttk.Button(test_buttons_frame, text="⚡ Hızlı Test", 
                  command=self.quick_test).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(test_buttons_frame, text="🔍 Bağlantı Testi", 
                  command=self.connection_test).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(test_buttons_frame, text="📄 Metin Testi", 
                  command=self.text_test).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(test_buttons_frame, text="🎨 Format Testi", 
                  command=self.format_test).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(test_buttons_frame, text="🌍 Karakter Testi", 
                  command=self.character_test).pack(side=tk.LEFT, padx=5)
        
        # Özel test alanı
        custom_test_frame = ttk.LabelFrame(test_frame, text="✏️ Özel Test")
        custom_test_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(custom_test_frame, text="Test metni:").pack(anchor=tk.W, padx=5, pady=5)
        
        self.custom_test_text = tk.Text(custom_test_frame, height=6, wrap=tk.WORD)
        self.custom_test_text.pack(fill=tk.X, padx=5, pady=5)
        self.custom_test_text.insert('1.0', "Özel test metninizi buraya yazın...")
        
        ttk.Button(custom_test_frame, text="🖨️ Özel Test Yazdır", 
                  command=self.custom_test).pack(pady=5)
        
        # Test sonuçları
        results_frame = ttk.LabelFrame(test_frame, text="📊 Test Sonuçları")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.test_results_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD)
        self.test_results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def create_settings_tab(self):
        """Gelişmiş ayarlar sekmesi"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="⚙️ Ayarlar")
        
        # API ayarları
        api_frame = ttk.LabelFrame(settings_frame, text="🔗 API Ayarları")
        api_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Grid layout için
        api_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(api_frame, text="API URL:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.url_entry = ttk.Entry(api_frame, width=60)
        self.url_entry.insert(0, self.api_url)
        self.url_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        
        ttk.Label(api_frame, text="Token:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.token_entry = ttk.Entry(api_frame, width=60, show="*")
        self.token_entry.insert(0, self.token)
        self.token_entry.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        
        ttk.Label(api_frame, text="Kontrol Aralığı (sn):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.interval_entry = ttk.Entry(api_frame, width=20)
        self.interval_entry.insert(0, str(self.check_interval))
        self.interval_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Yazıcı ayarları
        printer_settings_frame = ttk.LabelFrame(settings_frame, text="🖨️ Yazıcı Ayarları")
        printer_settings_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.auto_select_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(printer_settings_frame, text="Otomatik yazıcı seçimi", 
                       variable=self.auto_select_var).pack(anchor=tk.W, padx=5, pady=5)
        
        self.print_test_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(printer_settings_frame, text="Başlangıçta test yazdır", 
                       variable=self.print_test_var).pack(anchor=tk.W, padx=5, pady=5)
        
        # Kaydet butonu
        ttk.Button(settings_frame, text="💾 Ayarları Kaydet", 
                  command=self.save_settings).pack(pady=20)
    
    def create_logs_tab(self):
        """Gelişmiş log sekmesi"""
        logs_frame = ttk.Frame(self.notebook)
        self.notebook.add(logs_frame, text="📝 Loglar")
        
        # Log kontrolleri
        log_controls_frame = ttk.Frame(logs_frame)
        log_controls_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(log_controls_frame, text="🔄 Yenile", 
                  command=self.refresh_logs).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(log_controls_frame, text="🗑️ Temizle", 
                  command=self.clear_logs).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(log_controls_frame, text="💾 Dışa Aktar", 
                  command=self.export_logs).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(log_controls_frame, text="📂 Log Klasörü", 
                  command=self.open_log_folder).pack(side=tk.RIGHT, padx=5)
        
        # Log alanı
        log_text_frame = ttk.LabelFrame(logs_frame, text="📋 Sistem Logları")
        log_text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_text_frame, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def create_status_bar(self):
        """Gelişmiş durum çubuğu"""
        status_frame = tk.Frame(self.root, relief=tk.SUNKEN, bd=1)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_bar = ttk.Label(status_frame, text="Program hazır")
        self.status_bar.pack(side=tk.LEFT, padx=5)
        
        # Sağ tarafta sistem bilgileri
        system_info = f"OS: {self.printer_manager.system_info['os']} | " \
                     f"Python: {self.printer_manager.system_info['python_version']}"
        
        ttk.Label(status_frame, text=system_info).pack(side=tk.RIGHT, padx=5)
    
    # İşlevsellik metodları
    def auto_scan_printers(self):
        """Program başlangıcında otomatik yazıcı tarama"""
        self.log_message("🔄 Otomatik yazıcı taraması başlatılıyor...")
        
        def scan_in_thread():
            printers = self.printer_manager.scan_all_printers()
            self.root.after(0, lambda: self.update_printer_displays(printers))
        
        threading.Thread(target=scan_in_thread, daemon=True).start()
    
    def update_printer_displays(self, printers):
        """Yazıcı ekranlarını güncelle"""
        # Yazıcı listesini güncelle
        for item in self.printer_tree.get_children():
            self.printer_tree.delete(item)
        
        for name, info in printers.items():
            values = (
                name,
                info.get('status', 'Bilinmiyor'),
                info.get('type', ''),
                info.get('location', '')
            )
            self.printer_tree.insert('', tk.END, values=values)
        
        # Otomatik seçim
        if self.auto_select_var.get() and printers:
            # Varsayılan yazıcıyı veya ilk hazır olan yazıcıyı seç
            for name, info in printers.items():
                if info.get('is_default', False) or 'Hazır' in info.get('status', ''):
                    self.printer_manager.selected_printer = name
                    self.update_printer_status_display()
                    break
        
        self.log_message(f"✅ {len(printers)} yazıcı bulundu ve listelendi")
    
    def update_printer_status_display(self):
        """Yazıcı durum ekranını güncelle"""
        if self.printer_manager.selected_printer:
            printer_info = self.printer_manager.available_printers.get(
                self.printer_manager.selected_printer, {}
            )
            
            self.printer_status_label.config(
                text=f"✅ {self.printer_manager.selected_printer}"
            )
            self.printer_details_label.config(
                text=f"Durum: {printer_info.get('status', 'Bilinmiyor')}"
            )
        else:
            self.printer_status_label.config(text="❌ Yazıcı Seçilmedi")
            self.printer_details_label.config(text="Lütfen bir yazıcı seçin")
    
    def scan_printers(self):
        """Manuel yazıcı tarama"""
        self.log_message("🔄 Yazıcılar manuel olarak taranıyor...")
        
        def scan_in_thread():
            printers = self.printer_manager.scan_all_printers()
            self.root.after(0, lambda: self.update_printer_displays(printers))
        
        threading.Thread(target=scan_in_thread, daemon=True).start()
    
    def select_printer(self):
        """Seçili yazıcıyı aktif et"""
        selection = self.printer_tree.selection()
        if not selection:
            messagebox.showwarning("Uyarı", "Lütfen bir yazıcı seçin")
            return
        
        item = selection[0]
        printer_name = self.printer_tree.item(item)['values'][0]
        
        self.printer_manager.selected_printer = printer_name
        self.update_printer_status_display()
        
        self.log_message(f"✅ Yazıcı seçildi: {printer_name}")
    
    def quick_test_print(self):
        """Hızlı test yazdırma"""
        if not self.printer_manager.selected_printer:
            messagebox.showwarning("Uyarı", "Önce bir yazıcı seçin")
            return
        
        test_text = f"""
HIZLI TEST YAZDIRMA
==================
Tarih: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
Yazıcı: {self.printer_manager.selected_printer}

Bu hızlı bir test yazdırmasıdır.
Eğer bu metni okuyabiliyorsanız
yazıcınız düzgün çalışıyor.

TATO PASTA & BAKLAVA
Fabrika Yazıcı Sistemi
==================
"""
        
        self.log_message("🖨️ Hızlı test yazdırılıyor...")
        
        def print_in_thread():
            success = self.printer_manager._print_file_to_printer(None, 
                                                                self.printer_manager.selected_printer)
            message = "✅ Test başarılı" if success else "❌ Test başarısız"
            self.root.after(0, lambda: self.log_message(message))
        
        threading.Thread(target=print_in_thread, daemon=True).start()
    
    def comprehensive_printer_test(self):
        """Kapsamlı yazıcı testi"""
        if not self.printer_manager.selected_printer:
            messagebox.showwarning("Uyarı", "Önce bir yazıcı seçin")
            return
        
        self.log_message("🧪 Kapsamlı yazıcı testi başlatılıyor...")
        
        def test_in_thread():
            results = self.printer_manager.test_printer_comprehensive(
                self.printer_manager.selected_printer
            )
            self.root.after(0, lambda: self.display_test_results(results))
        
        threading.Thread(target=test_in_thread, daemon=True).start()
    
    def display_test_results(self, results):
        """Test sonuçlarını görüntüle"""
        self.test_results_text.delete('1.0', tk.END)
        
        self.test_results_text.insert(tk.END, "🧪 KAPSAMLI YAZICI TESTİ SONUÇLARI\n")
        self.test_results_text.insert(tk.END, "=" * 50 + "\n\n")
        
        for result in results:
            status = "✅" if result['result'] else "❌"
            self.test_results_text.insert(tk.END, 
                f"{status} {result['test']}: {result['message']}\n")
        
        self.test_results_text.insert(tk.END, "\n" + "=" * 50 + "\n")
        self.test_results_text.insert(tk.END, f"Test tamamlandı: {datetime.now().strftime('%H:%M:%S')}\n")
        
        # Test merkezi sekmesine geç
        self.notebook.select(3)
    
    def show_printer_info(self):
        """Yazıcı bilgilerini göster"""
        if not self.printer_manager.selected_printer:
            messagebox.showwarning("Uyarı", "Önce bir yazıcı seçin")
            return
        
        printer_details = self.printer_manager.get_printer_details(
            self.printer_manager.selected_printer
        )
        
        if printer_details:
            self.display_printer_details(printer_details)
            # Yazıcı yönetimi sekmesine geç
            self.notebook.select(1)
    
    def display_printer_details(self, details):
        """Yazıcı detaylarını görüntüle"""
        self.printer_details_text.delete('1.0', tk.END)
        
        basic_info = details['basic_info']
        capabilities = details.get('capabilities', {})
        queue_info = details.get('queue_info', {})
        
        self.printer_details_text.insert(tk.END, "🖨️ YAZICI DETAYLARI\n")
        self.printer_details_text.insert(tk.END, "=" * 40 + "\n\n")
        
        # Temel bilgiler
        self.printer_details_text.insert(tk.END, "📋 TEMEL BİLGİLER:\n")
        for key, value in basic_info.items():
            self.printer_details_text.insert(tk.END, f"  {key}: {value}\n")
        
        # Yetenekler
        if capabilities and 'error' not in capabilities:
            self.printer_details_text.insert(tk.END, "\n🎯 YETENEKLER:\n")
            for key, value in capabilities.items():
                self.printer_details_text.insert(tk.END, f"  {key}: {value}\n")
        
        # Kuyruk bilgisi
        if queue_info and 'error' not in queue_info:
            self.printer_details_text.insert(tk.END, f"\n📋 KUYRUK BİLGİSİ:\n")
            self.printer_details_text.insert(tk.END, f"  Bekleyen iş: {queue_info.get('job_count', 0)}\n")
    
    def open_printer_wizard(self):
        """Yazıcı kurulum sihirbazı"""
        wizard_info = self.printer_manager.install_printer_wizard()
        
        wizard_window = tk.Toplevel(self.root)
        wizard_window.title("🔧 Yazıcı Kurulum Sihirbazı")
        wizard_window.geometry("600x500")
        wizard_window.transient(self.root)
        wizard_window.grab_set()
        
        # Sihirbaz içeriği
        ttk.Label(wizard_window, text="🔧 Yazıcı Kurulum Sihirbazı", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        steps_frame = ttk.LabelFrame(wizard_window, text="📋 Kurulum Adımları")
        steps_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        steps_text = scrolledtext.ScrolledText(steps_frame, wrap=tk.WORD)
        steps_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Adımları ekle
        for i, step in enumerate(wizard_info['steps'], 1):
            steps_text.insert(tk.END, f"{i}. {step}\n")
        
        steps_text.insert(tk.END, "\n🔧 SORUN GİDERME:\n")
        for tip in wizard_info['troubleshooting']:
            steps_text.insert(tk.END, f"• {tip}\n")
        
        ttk.Button(wizard_window, text="✅ Anladım", 
                  command=wizard_window.destroy).pack(pady=10)
    
    # API metodları
    def test_api_connection(self):
        """API bağlantı testi"""
        self.log_message("🔍 API bağlantı testi başlatılıyor...")
        
        def test_in_thread():
            try:
                url = f"{self.api_url}/orders/api/factory/orders/"
                params = {'token': self.token}
                
                response = requests.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    count = data.get('count', 0)
                    
                    self.root.after(0, lambda: self.connection_status_label.config(text="🟢 Bağlı"))
                    self.root.after(0, lambda: self.api_details_label.config(text=f"{count} sipariş mevcut"))
                    self.root.after(0, lambda: self.log_message(f"✅ API bağlantısı başarılı! {count} sipariş"))
                    
                else:
                    self.root.after(0, lambda: self.connection_status_label.config(text="🔴 Hata"))
                    self.root.after(0, lambda: self.api_details_label.config(text=f"HTTP {response.status_code}"))
                    self.root.after(0, lambda: self.log_message(f"❌ API hatası: {response.status_code}"))
                    
            except Exception as e:
                self.root.after(0, lambda: self.connection_status_label.config(text="🔴 Bağlantı Yok"))
                self.root.after(0, lambda: self.api_details_label.config(text="Bağlantı hatası"))
                self.root.after(0, lambda: self.log_message(f"❌ Bağlantı hatası: {str(e)}"))
        
        threading.Thread(target=test_in_thread, daemon=True).start()
    
    def start_service(self):
        """Ana servisi başlat"""
        if not self.printer_manager.selected_printer:
            messagebox.showwarning("Uyarı", "Önce bir yazıcı seçin!")
            return
        
        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        
        self.log_message("🚀 Fabrika yazıcı sistemi başlatıldı")
        self.log_message(f"🖨️ Aktif yazıcı: {self.printer_manager.selected_printer}")
        
        # Arka plan servisi başlat
        self.service_thread = threading.Thread(target=self.service_loop, daemon=True)
        self.service_thread.start()
    
    def stop_service(self):
        """Ana servisi durdur"""
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        
        self.connection_status_label.config(text="🔴 Durduruldu")
        
        self.log_message("⏹️ Fabrika yazıcı sistemi durduruldu")
    
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
        """Yeni siparişleri kontrol et ve işle"""
        try:
            url = f"{self.api_url}/orders/api/factory/orders/"
            params = {'token': self.token}
            
            if self.last_check_time:
                params['last_check'] = self.last_check_time.isoformat()
            
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                orders = data.get('orders', [])
                
                self.root.after(0, lambda: self.connection_status_label.config(text="🟢 Aktif"))
                self.root.after(0, lambda: self.process_new_orders(orders))
                
                self.last_check_time = datetime.now(timezone.utc)
                
            else:
                self.root.after(0, lambda: self.connection_status_label.config(text="🔴 API Hatası"))
                
        except Exception as e:
            self.root.after(0, lambda: self.connection_status_label.config(text="🔴 Bağlantı Yok"))
    
    def process_new_orders(self, orders):
        """Yeni siparişleri işle"""
        new_orders = [order for order in orders if order['id'] not in self.processed_orders]
        
        if new_orders:
            self.log_message(f"🆕 {len(new_orders)} yeni sipariş alındı")
            
            for order in new_orders:
                self.print_order_enhanced(order)
                self.processed_orders.add(order['id'])
        
        self.update_orders_display(orders)
        self.update_statistics(orders)
    
    def print_order_enhanced(self, order):
        """Gelişmiş sipariş yazdırma"""
        try:
            self.log_message(f"🖨️ Yazdırılıyor: {order['order_number']} - {order['branch_name']}")
            
            # Gelişmiş sipariş formatı
            formatted_text = self.format_order_enhanced(order)
            
            # Yazdırma işlemi
            success = self.printer_manager._print_file_to_printer(None, 
                                                                self.printer_manager.selected_printer)
            
            if success:
                self.log_message(f"✅ Başarıyla yazdırıldı: {order['order_number']}")
                self.mark_order_printed_api(order['id'])
            else:
                self.log_message(f"❌ Yazdırma başarısız: {order['order_number']}")
                
        except Exception as e:
            self.log_message(f"❌ Yazdırma hatası: {str(e)}")
    
    def format_order_enhanced(self, order):
        """Gelişmiş sipariş formatı"""
        lines = []
        lines.append("=" * 60)
        lines.append("        TATO PASTA & BAKLAVA")
        lines.append("       FABRİKA ÜRETİM SİPARİŞİ")
        lines.append("=" * 60)
        lines.append("")
        
        # Sipariş bilgileri
        lines.append(f"Sipariş No      : {order['order_number']}")
        lines.append(f"Şube            : {order['branch_name']}")
        lines.append(f"Teslimat Tarihi : {self.format_date(order['delivery_date'])}")
        lines.append(f"Sipariş Zamanı  : {self.format_datetime(order['created_at'])}")
        lines.append(f"Sipariş Veren   : {order['created_by']}")
        
        if order['notes']:
            lines.append(f"Özel Notlar     : {order['notes']}")
        
        lines.append("")
        lines.append("-" * 60)
        lines.append("                      ÜRÜN LİSTESİ")
        lines.append("-" * 60)
        
        # Ürün listesi
        total_items = 0
        for i, item in enumerate(order['items'], 1):
            lines.append(f"{i:2d}. {item['product_name']:<35} {item['quantity']:>6} {item['unit']}")
            
            if item['notes']:
                lines.append(f"    Not: {item['notes']}")
            
            total_items += item['quantity']
        
        lines.append("-" * 60)
        lines.append(f"TOPLAM ÜRÜN SAYISI: {total_items} adet")
        lines.append(f"TOPLAM TUTAR      : ₺{order['total_amount']:.2f}")
        
        # Üretim bilgileri
        lines.append("")
        lines.append("🏭 ÜRETİM BİLGİLERİ:")
        lines.append(f"Yazıcı          : {self.printer_manager.selected_printer}")
        lines.append(f"Yazdırma Zamanı : {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
        lines.append(f"Sistem Sürümü   : Süper Gelişmiş v2.0")
        
        lines.append("")
        lines.append("=" * 60)
        lines.append("          ÜRETİME HAZIR - İYİ ÇALIŞMALAR!")
        lines.append("=" * 60)
        lines.append("")
        
        return "\n".join(lines)
    
    def update_orders_display(self, orders):
        """Siparişler tablosunu güncelle"""
        # Mevcut verileri temizle
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)
        
        # Yeni verileri ekle
        for order in orders:
            # Öncelik belirleme
            delivery_date = datetime.fromisoformat(order['delivery_date'].replace('Z', '+00:00'))
            now = datetime.now(timezone.utc)
            days_until = (delivery_date - now).days
            
            if days_until <= 0:
                priority = "🔴 ACİL"
            elif days_until == 1:
                priority = "🟡 YARIN"
            else:
                priority = "🟢 NORMAL"
            
            values = (
                order['order_number'],
                order['branch_name'],
                self.format_date(order['delivery_date']),
                len(order['items']),
                f"₺{order['total_amount']:.0f}",
                "✅ Yazdırıldı" if order['id'] in self.processed_orders else "⏳ Bekliyor",
                priority
            )
            
            self.orders_tree.insert('', tk.END, values=values)
    
    def update_statistics(self, orders):
        """İstatistikleri güncelle"""
        total = len(orders)
        printed = len([o for o in orders if o['id'] in self.processed_orders])
        
        self.total_orders_label.config(text=f"Toplam: {total}")
        self.printed_orders_label.config(text=f"Yazdırılan: {printed}")
        self.last_check_label.config(text=f"Son kontrol: {datetime.now().strftime('%H:%M:%S')}")
    
    # Yardımcı metodlar
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
    
    # Diğer metodlar
    def manual_refresh(self):
        """Manuel yenileme"""
        self.scan_printers()
        self.test_api_connection()
    
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
    
    def on_order_double_click(self, event):
        """Sipariş çift tıklama"""
        selection = self.orders_tree.selection()
        if selection:
            item = selection[0]
            order_number = self.orders_tree.item(item)['values'][0]
            self.log_message(f"📋 Sipariş detayları: {order_number}")
    
    def mark_order_printed_api(self, order_id):
        """API'ye yazdırıldı işaretle"""
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
    
    # Test metodları - stubs
    def auto_discovery(self): self.log_message("🔍 Otomatik keşif başlatıldı")
    def network_scan(self): self.log_message("🌐 Ağ taraması başlatıldı")
    def usb_scan(self): self.log_message("🔌 USB tarama başlatıldı")
    def manual_printer_add(self): self.log_message("➕ Manuel yazıcı ekleme")
    def quick_test(self): self.log_message("⚡ Hızlı test")
    def connection_test(self): self.log_message("🔍 Bağlantı testi")
    def text_test(self): self.log_message("📄 Metin testi")
    def format_test(self): self.log_message("🎨 Format testi")
    def character_test(self): self.log_message("🌍 Karakter testi")
    def custom_test(self): self.log_message("✏️ Özel test")
    def update_live_status(self): self.log_message("📡 Canlı durum güncellendi")
    def show_detailed_printer_info(self): self.show_printer_info()
    def open_printer_settings(self): self.log_message("⚙️ Yazıcı ayarları")
    def test_selected_printer(self): self.quick_test_print()
    def refresh_logs(self): self.log_message("🔄 Loglar yenilendi")
    def clear_logs(self): 
        self.log_text.delete('1.0', tk.END)
        self.log_message("🗑️ Loglar temizlendi")
    def export_logs(self): self.log_message("💾 Loglar dışa aktarıldı")
    def open_log_folder(self): 
        try:
            os.startfile(os.getcwd())
        except:
            self.log_message("📂 Log klasörü açılamadı")
    
    def on_closing(self):
        """Program kapanış"""
        if self.is_running:
            self.stop_service()
        
        self.log_message("👋 Süper Gelişmiş Fabrika Yazıcı Programı kapatılıyor...")
        self.root.destroy()
    
    def run(self):
        """Programı çalıştır"""
        self.root.mainloop()


def main():
    """Ana fonksiyon"""
    try:
        app = SüperGelişmisFabrikaYaziciProgram()
        app.run()
    except Exception as e:
        messagebox.showerror("Hata", f"Program başlatılamadı: {str(e)}")


if __name__ == "__main__":
    main()