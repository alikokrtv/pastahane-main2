from datetime import timedelta

from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from django.utils import timezone

from pos.models import Satislar


def kpi_today():
    # bugünkü satış ve ortalama fiş tutarı
    today_qs = Satislar.objects.filter(tarih__date=timezone.now().date())
    ciro = today_qs.aggregate(ciro=Sum("toplam"))["ciro"] or 0
    fis = today_qs.values("fisno").distinct().count()
    avg_fis = (ciro / fis) if fis else 0
    return {"ciro": ciro, "fis_sayisi": fis, "ortalama_fis": avg_fis}


def revenue_by_day(days=7):
    qs = Satislar.objects.filter(tarih__gte=timezone.now() - timedelta(days=days))
    return list(
        qs.annotate(gun=TruncDate("tarih")).values("gun").annotate(ciro=Sum("toplam")).order_by("gun")
    )


def payment_distribution():
    qs = (
        Satislar.objects.values("odemesi")
        .annotate(ciro=Sum("toplam"), fis=Count("fisno", distinct=True))
        .order_by("-ciro")
    )
    return list(qs)


def top_products(limit=10):
    qs = (
        Satislar.objects.values("urun")
        .annotate(ciro=Sum("toplam"), adet=Sum("adet"))
        .order_by("-ciro")
    )
    return list(qs[:limit])
