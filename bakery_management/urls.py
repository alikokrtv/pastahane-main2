"""
URL configuration for bakery_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from . import views

# Admin site başlık ve başlık ayarları
admin.site.site_header = "Pastane Yönetim Sistemi"
admin.site.site_title = "Pastane Yönetimi"
admin.site.index_title = "Yönetim Paneli"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Login/logout URLs
    path('', views.home, name='home'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    # API endpoints
    path('api/users/', include(('users.urls', 'users-api'), namespace='users-api')),
    path('api/orders/', include(('orders.urls', 'orders-api'), namespace='orders-api')),
    path('api/inventory/', include(('inventory.urls', 'inventory-api'), namespace='inventory-api')),
    path('api/production/', include(('production.urls', 'production-api'), namespace='production-api')),
    path('api/sales/', include(('sales.urls', 'sales-api'), namespace='sales-api')),
    path('api/reports/', include(('reports.urls', 'reports-api'), namespace='reports-api')),
    
    # Web views
    path('users/', include('users.urls')),
    path('orders/', include('orders.urls')),
    path('inventory/', include('inventory.urls')),
    path('production/', include('production.urls')),
    path('sales/', include('sales.urls')),
    path('reports/', include('reports.urls')),
]

# Static ve media dosyalar için development ayarları
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
