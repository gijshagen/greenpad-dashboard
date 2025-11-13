from django.db import models


class Trade(models.Model):
    BROKER_CHOICES = [
        ("DEGIRO", "DeGiro"),
        ("IBKR", "Interactive Brokers"),
        ("OTHER", "Other"),
    ]

    broker = models.CharField(
        max_length=20,
        choices=BROKER_CHOICES,
        default="IBKR",
    )
    symbol = models.CharField(max_length=50)
    isin = models.CharField(max_length=12, blank=True, null=True)
    trade_datetime = models.DateTimeField()
    side = models.CharField(max_length=10)  # BUY / SELL
    quantity = models.DecimalField(max_digits=20, decimal_places=4)
    price = models.DecimalField(max_digits=20, decimal_places=4)
    fee = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    currency = models.CharField(max_length=10, default="EUR")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol} {self.side} {self.quantity} @ {self.price} ({self.broker})"
