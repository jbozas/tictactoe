from django.db import models
from .timestampmodel import TimeStampModel


class Movement(TimeStampModel):
    player_name = models.CharField(max_length=256)
    destination = models.CharField(max_length=2)

    def __str__(self) -> str:
        return f"Movement by {self.player_name} - row: {self.destination[0]}, column:  {self.destination[1]})"
