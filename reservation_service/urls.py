from django.urls import path
from . import views

urlpatterns = [
    path('reservation/<int:movie_id>', views.get_all_showtimes),
    path('reservation/<int:movie_id>/<int:showtime_id>', views.get_seat),
    path('reservation/<int:movie_id>/create', views.create_showtime)
]