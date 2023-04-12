from django.urls import path
from . import views

urlpatterns = [
    path('reservation/movie=<int:movie>/showtime', views.get_seat),
]