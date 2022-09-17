from django.db import models
from django.utils.timezone import now


class Blockchain(models.Model):
    class Categories(models.TextChoices):
        NO_DEF = "Not Selected"
        LAYER_1 = "Layer 1"
        LAYER_2 = "Layer 2"
        DEFI = "DeFi"
        BRIDGE = "Bridge"

    name = models.CharField(max_length=50, unique=True)
    ticker = models.CharField(max_length=10, unique=True)
    type = models.CharField(
        choices=Categories.choices, default=Categories.NO_DEF, max_length=30
    )
    last_update = models.DateTimeField(default=now, editable=True)
    project_url = models.URLField(blank=True)
    market_cap = models.IntegerField(default=0)
    last_price = models.FloatField(default=0, max_length=20)
    notes = models.CharField(max_length=200, default="")

    objects = models.Manager()  # helps with reference to django object attribute

    def __str__(self) -> str:
        return f"{self.name} ({self.ticker})"
