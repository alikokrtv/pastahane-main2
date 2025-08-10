#!/usr/bin/env python
import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bakery_management.settings')
django.setup()

from django.core.cache import cache
from django.core.management import call_command

print("Cache temizleniyor...")
cache.clear()
print("Cache temizlendi!")

print("Static files toplanıyor...")
call_command('collectstatic', '--noinput')
print("Static files toplandı!")

print("İşlem tamamlandı!")
