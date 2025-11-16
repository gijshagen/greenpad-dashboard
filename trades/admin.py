from django.contrib import admin
from .models import Trade


@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = (
        "trade_datetime",
        "symbol",
        "side",
        "quantity",
        "price",
        "currency",
        "broker",
    )
    list_filter = ("broker", "symbol", "side", "currency")
    search_fields = ("symbol", "isin")
    ordering = ("-trade_datetime",)
