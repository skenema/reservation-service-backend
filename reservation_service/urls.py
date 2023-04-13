from django.urls import path
from . import views

urlpatterns = [
    path('reservation/<int:movie>/showtime', views.get_seat),
]