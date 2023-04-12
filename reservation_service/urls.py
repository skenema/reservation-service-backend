from django.urls import path
from . import views

urlpatterns = [
    path('reservation/movie=<str:movie>/showtime', views.get_seat),
]