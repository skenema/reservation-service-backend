from django.urls import path
from . import views

urlpatterns = [
    path('reservation/<int:movie_id>', views.get_all_showtimes),
    path('reservatin/<int:movie_id>/init', views.initialize_reservation),
    path('reservation/<int:movie_id>/<int:showtime_id>', views.get_seat),
]