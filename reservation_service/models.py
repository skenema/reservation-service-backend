from django.db import models
from datetime import datetime

class Seat(models.Model):
    title_movie = models.CharField(max_length=255)
    show_time = models.DateTimeField(default=datetime.now())
    seat_id = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.title_movie} seat {self.seat_id} is available: {self.is_available}"

