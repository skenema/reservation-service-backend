from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Seat
from rest_framework.response import Response

@api_view(['GET', 'POST'])
def get_seat(request, movie):
    data = request.data
    if request.method == 'GET':
        array_seat_object = Seat.objects.filter(title_movie=movie)
        if not array_seat_object:
            for i in range(10):
                seat = Seat.objects.create  (   title_movie = movie,
                                                showtime    = data["showtime"],
                                                seat_id     = i+1,
                                                is_available = True 
                                            )
                seat.save() 
        array_seat = []        
        for i in range(len(array_seat_object)):
            array_seat.append({ "seat_id": array_seat_object[i].seat_id,
                                "is_available": array_seat_object[i].is_available
                            })
        return Response(array_seat)
    elif request.method == 'POST':
        seat_object = Seat.objects.filter(  title_movie=movie,
                                            seat_id=data["seat_id"]).update(is_available = False)
        response = {    "seat_ticket": data["seat_id"],
                        "showtime": data["showtime"]}
        return Response(response)



