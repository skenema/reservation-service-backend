from django.urls import path
from . import views

urlpatterns = [
    path('reservation/<int:movie_id>/<int:showtime_id>', views.get_seat), # TODO: Change to individual showtime ID.
    path('reservation/<int:movie_id>/showtimes', views.get_all_showtimes)
]