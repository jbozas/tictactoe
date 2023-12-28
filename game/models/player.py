from django.db import models


class Player(models.Model):
    symbol = models.CharField(max_length=5)
    name = models.CharField(max_length=255)

    class Meta:
        app_label = "game"

    def __str__(self) -> str:
        return f"Player {self.name}, symbol: ({self.symbol})"
