# ViaPos Dashboard Utility Functions
from django.db import connections
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

def get_viapos_connection():
    """ViaPos veritabanı bağlantısını al"""
    try:
        return connections['viapos']
    except Exception as e:
        logger.error(f"ViaPos veritabanı bağlantısı hatası: {e}")
        return None

def execute_viapos_query(query, params=None):
    """ViaPos veritabanında sorgu çalıştır"""
    connection = get_viapos_connection()
    if not connection:
        return []
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params or [])
            columns = [col[0] for col in cursor.description]
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            return results
    except Exception as e:
        logger.error(f"ViaPos sorgu hatası: {e}")
        return []

def get_pasta_summary():
    """Pasta/dilim/turta benzeri ürünler için özet verisi (urunler tablosu)."""
    query = """
    SELECT 
        urun,
        satis,
        birin,
        grub,
        kayittarih
    FROM urunler
    WHERE (
        LOWER(urun) LIKE '%pasta%' OR 
        LOWER(urun) LIKE '%dilim%' OR 
        LOWER(urun) LIKE '%turta%' OR
        LOWER(urun) LIKE '%kek%' OR
        LOWER(urun) LIKE '%tart%'
    )
    ORDER BY urun
    """

    results = execute_viapos_query(query)

    # Kategori bazında gruplama
    categories = {
        'Dilim Pastalar': [],
        'Turta Pastalar': [],
        'Kekler': [],
        'Diğer Pastalar': []
    }

    total_items = 0
    total_value = Decimal('0')

    for item in results:
        total_items += 1
        try:
            price = Decimal(str(item.get('satis', 0) or 0))
            total_value += price
        except Exception:
            price = Decimal('0')

        name_lc = item.get('urun', '').lower()
        if 'dilim' in name_lc or 'parça' in name_lc:
            category = 'Dilim Pastalar'
        elif 'turta' in name_lc or 'büyük' in name_lc:
            category = 'Turta Pastalar'
        elif 'kek' in name_lc:
            category = 'Kekler'
        else:
            category = 'Diğer Pastalar'

        categories[category].append({
            'name': item.get('urun', ''),
            'price': float(price),
            'unit': item.get('birin', 'ADET'),
            'group': item.get('grub', ''),
            'date_added': item.get('kayittarih')
        })

    return {
        'categories': categories,
        'total_items': total_items,
        'total_value': float(total_value),
        'last_updated': timezone.now()
    }

def get_recent_sales():
    """Son satışları getir (satislar + fisno)."""
    query = """
    SELECT 
        s.id,
        s.fisno,
        s.tarih,
        s.musteriadi,
        s.toplam,
        s.urun,
        s.adet,
        s.fiyat
    FROM satislar s
    WHERE s.tarih >= DATE_SUB(NOW(), INTERVAL 7 DAY)
    ORDER BY s.tarih DESC
    LIMIT 10
    """

    results = execute_viapos_query(query)

    sales_data = []
    for sale in results:
        try:
            amount = Decimal(str(sale.get('toplam', 0) or 0))
        except Exception:
            amount = Decimal('0')

        sales_data.append({
            'code': sale.get('fisno'),
            'type': sale.get('urun'),
            'customer': sale.get('musteriadi', 'Bilinmeyen'),
            'amount': float(amount),
            'currency': 'TL',
            'date': sale.get('tarih')
        })

    return sales_data

def get_dashboard_stats():
    """Dashboard için genel istatistikler"""
    pasta_summary = get_pasta_summary()
    recent_sales = get_recent_sales()
    
    # Günlük satış toplamı (fisno.toplam)
    today_query = """
    SELECT COALESCE(SUM(toplam), 0) as daily_total
    FROM fisno
    WHERE DATE(tarih) = CURDATE()
    AND toplam > 0
    """
    
    daily_total_result = execute_viapos_query(today_query)
    daily_total = 0
    if daily_total_result:
        try:
            daily_total = float(daily_total_result[0].get('daily_total', 0) or 0)
        except:
            daily_total = 0
    
    # Haftalık satış toplamı (fisno.toplam)
    weekly_query = """
    SELECT COALESCE(SUM(toplam), 0) as weekly_total
    FROM fisno
    WHERE tarih >= DATE_SUB(NOW(), INTERVAL 7 DAY)
    AND toplam > 0
    """
    
    weekly_total_result = execute_viapos_query(weekly_query)
    weekly_total = 0
    if weekly_total_result:
        try:
            weekly_total = float(weekly_total_result[0].get('weekly_total', 0) or 0)
        except:
            weekly_total = 0
    
    return {
        'pasta_summary': pasta_summary,
        'recent_sales': recent_sales,
        'daily_total': daily_total,
        'weekly_total': weekly_total,
        'connection_status': get_viapos_connection() is not None
    }
