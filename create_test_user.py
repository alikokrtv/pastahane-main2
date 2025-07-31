#!/usr/bin/env python
"""
Test kullanıcısı oluşturma scripti
"""
import os
import sys
import django

# Django ayarlarını yükle
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bakery_management.settings')
django.setup()

from django.contrib.auth import get_user_model
from users.models import Branch

User = get_user_model()

def create_test_data():
    """Test verileri oluştur"""
    
    # Ana şube varsa al, yoksa oluştur
    branch, created = Branch.objects.get_or_create(
        name='Ana Şube',
        defaults={
            'address': 'Test Adres',
            'phone': '0212 123 45 67',
            'is_active': True
        }
    )
    
    if created:
        print(f"✓ Şube oluşturuldu: {branch.name}")
    else:
        print(f"✓ Şube mevcut: {branch.name}")
    
    # Test şube müdürü oluştur
    username = 'sube1'
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        print(f"✓ Kullanıcı mevcut: {username}")
    else:
        user = User.objects.create_user(
            username=username,
            password='123456',
            first_name='Ahmet',
            last_name='Yılmaz',
            email='sube1@pastane.com',
            branch=branch,
            is_active=True
        )
        print(f"✓ Şube müdürü oluşturuldu: {username} (şifre: 123456)")
    
    # Admin kullanıcı oluştur
    admin_username = 'admin'
    if User.objects.filter(username=admin_username).exists():
        admin = User.objects.get(username=admin_username)
        print(f"✓ Admin kullanıcı mevcut: {admin_username}")
    else:
        admin = User.objects.create_superuser(
            username=admin_username,
            password='admin123',
            email='admin@pastane.com',
            first_name='Admin',
            last_name='User'
        )
        print(f"✓ Admin kullanıcı oluşturuldu: {admin_username} (şifre: admin123)")
    
    print("\n" + "="*50)
    print("TEST KULLANICILARI HAZIR!")
    print("="*50)
    print(f"Şube Müdürü: {username} / 123456")
    print(f"Admin: {admin_username} / admin123")
    print("="*50)

if __name__ == '__main__':
    create_test_data()
