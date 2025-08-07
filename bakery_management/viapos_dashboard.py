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
    """Pasta dilimleri özet verisi"""
    query = """
    SELECT 
        stokadi,
        grup1,
        grup2,
        satis,
        birim,
        aktif,
        kayittarihi
    FROM stok 
    WHERE aktif = '1' 
    AND (
        LOWER(stokadi) LIKE '%pasta%' OR 
        LOWER(stokadi) LIKE '%dilim%' OR 
        LOWER(stokadi) LIKE '%turta%' OR
        LOWER(stokadi) LIKE '%kek%' OR
        LOWER(stokadi) LIKE '%tart%'
    )
    ORDER BY stokadi
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
        except:
            price = Decimal('0')
        
        # Kategori belirleme
        stok_adi = item.get('stokadi', '').lower()
        if 'dilim' in stok_adi or 'parça' in stok_adi:
            category = 'Dilim Pastalar'
        elif 'turta' in stok_adi or 'büyük' in stok_adi:
            category = 'Turta Pastalar'
        elif 'kek' in stok_adi:
            category = 'Kekler'
        else:
            category = 'Diğer Pastalar'
        
        categories[category].append({
            'name': item.get('stokadi', ''),
            'price': float(price),
            'unit': item.get('birim', 'ADET'),
            'group1': item.get('grup1', ''),
            'group2': item.get('grup2', ''),
            'date_added': item.get('kayittarihi')
        })
    
    return {
        'categories': categories,
        'total_items': total_items,
        'total_value': float(total_value),
        'last_updated': timezone.now()
    }

def get_recent_sales():
    """Son satışları getir"""
    query = """
    SELECT 
        h.hareketkodu,
        h.islem,
        h.firmaadi,
        h.toplam,
        h.kayittarihi,
        h.parabirimi
    FROM hareket h
    WHERE h.aktif = '1' 
    AND h.kayittarihi >= DATE_SUB(NOW(), INTERVAL 7 DAY)
    ORDER BY h.kayittarihi DESC
    LIMIT 10
    """
    
    results = execute_viapos_query(query)
    
    sales_data = []
    for sale in results:
        try:
            amount = Decimal(str(sale.get('toplam', 0) or 0))
        except:
            amount = Decimal('0')
        
        sales_data.append({
            'code': sale.get('hareketkodu'),
            'type': sale.get('islem'),
            'customer': sale.get('firmaadi', 'Bilinmeyen'),
            'amount': float(amount),
            'currency': sale.get('parabirimi', 'TL'),
            'date': sale.get('kayittarihi')
        })
    
    return sales_data

def get_dashboard_stats():
    """Dashboard için genel istatistikler"""
    pasta_summary = get_pasta_summary()
    recent_sales = get_recent_sales()
    
    # Günlük satış toplamı
    today_query = """
    SELECT COALESCE(SUM(toplam), 0) as daily_total
    FROM hareket 
    WHERE aktif = '1' 
    AND DATE(kayittarihi) = CURDATE()
    AND toplam > 0
    """
    
    daily_total_result = execute_viapos_query(today_query)
    daily_total = 0
    if daily_total_result:
        try:
            daily_total = float(daily_total_result[0].get('daily_total', 0) or 0)
        except:
            daily_total = 0
    
    # Haftalık satış toplamı
    weekly_query = """
    SELECT COALESCE(SUM(toplam), 0) as weekly_total
    FROM hareket 
    WHERE aktif = '1' 
    AND kayittarihi >= DATE_SUB(NOW(), INTERVAL 7 DAY)
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
