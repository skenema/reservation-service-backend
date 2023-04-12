from django.db import models
from datetime import datetime

class Showtime(models.Model):
    movie_id = models.IntegerField(default=0)
    showtime = models.DateTimeField(null=False)

    def __str__(self) -> str:
        return f"{self.movie_id}: {self.showtime}"

class Seat(models.Model):
    showtime_id = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    seat_id = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.showtime_id} seat {self.seat_id} is available: {self.is_available}"

