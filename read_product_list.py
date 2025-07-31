#!/usr/bin/env python
"""
Excel ürün listesini okuyup analiz et
"""
import pandas as pd
import os

def read_product_excel():
    """Excel dosyasından ürün listesini oku"""
    try:
        excel_file = "YENİ PASTA  LİSTE YAZILIM.xlsx"
        
        if not os.path.exists(excel_file):
            print(f"❌ Excel dosyası bulunamadı: {excel_file}")
            return None
        
        print(f"📊 Excel dosyası okunuyor: {excel_file}")
        
        # Excel dosyasını oku
        df = pd.read_excel(excel_file)
        
        print(f"✅ Excel dosyası başarıyla okundu!")
        print(f"   Toplam satır sayısı: {len(df)}")
        print(f"   Sütun sayısı: {len(df.columns)}")
        
        print("\n📋 Sütun isimleri:")
        for i, col in enumerate(df.columns, 1):
            print(f"   {i}. {col}")
        
        print("\n📝 İlk 10 ürün:")
        print(df.head(10).to_string(index=False))
        
        # Boş olmayan satırları say
        non_empty_rows = df.dropna(how='all')
        print(f"\n📊 İstatistikler:")
        print(f"   Boş olmayan satır sayısı: {len(non_empty_rows)}")
        
        # Her sütundaki boş olmayan değer sayısı
        print("\n📈 Sütun bazında dolu veri sayısı:")
        for col in df.columns:
            non_null_count = df[col].notna().sum()
            print(f"   {col}: {non_null_count} dolu veri")
        
        return df
        
    except Exception as e:
        print(f"❌ Excel okuma hatası: {e}")
        return None

def analyze_product_structure(df):
    """Ürün yapısını analiz et"""
    if df is None:
        return
    
    print("\n🔍 Ürün yapısı analizi:")
    
    # Muhtemel ürün adı sütununu bul
    possible_name_columns = []
    for col in df.columns:
        col_lower = str(col).lower()
        if any(keyword in col_lower for keyword in ['ürün', 'product', 'name', 'ad', 'isim', 'pasta']):
            possible_name_columns.append(col)
    
    if possible_name_columns:
        print(f"   Muhtemel ürün adı sütunları: {possible_name_columns}")
        
        # İlk muhtemel sütundaki örnek değerler
        first_col = possible_name_columns[0]
        sample_values = df[first_col].dropna().head(5).tolist()
        print(f"   '{first_col}' sütunundaki örnek değerler: {sample_values}")
    
    # Muhtemel fiyat sütununu bul
    possible_price_columns = []
    for col in df.columns:
        col_lower = str(col).lower()
        if any(keyword in col_lower for keyword in ['fiyat', 'price', 'tutar', 'ücret', 'tl']):
            possible_price_columns.append(col)
    
    if possible_price_columns:
        print(f"   Muhtemel fiyat sütunları: {possible_price_columns}")
    
    # Sayısal sütunları bul
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    if numeric_columns:
        print(f"   Sayısal sütunlar: {numeric_columns}")

if __name__ == "__main__":
    print("Excel ürün listesi analiz ediliyor...\n")
    
    df = read_product_excel()
    if df is not None:
        analyze_product_structure(df)
        print("\n✅ Excel analizi tamamlandı!")
    else:
        print("\n❌ Excel analizi başarısız!")
