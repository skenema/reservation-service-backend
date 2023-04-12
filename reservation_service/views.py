from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Seat, Showtime
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

@api_view(['GET', 'POST'])
def get_seat(request, movie):
    if request.method == 'GET':
        try:
            showtime_object = Showtime.objects.get(movie_id=movie)  
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND) 

        showtime_object = Showtime.objects.get(movie_id=movie)  
        seat_object = Seat.objects.filter(showtime_id = showtime_object)
        if not seat_object:
            for i in range(10):
                Seat.objects.create(    showtime_id = showtime_object,
                                        seat_id = i+1,
                                        is_available = True)
        array_seat = []
        for i in  range(len(seat_object)):
            array_seat.append({     "seat_id": seat_object[i].seat_id,
                                    "showtime_id": seat_object[i].is_available

            })
        return Response(array_seat)
    elif request.method == 'POST':
        data = request.data
        for i in data["seat_id"]:
            showtime_object = Showtime.objects.get(movie_id=movie)   
            seat_object = Seat.objects.get(  showtime_id = showtime_object, 
                                            seat_id = i)
            if seat_object.is_available == False:
                return Response("Fail to reserve")
        
        array_seat = []
        for i in data["seat_id"]:
            showtime_object = Showtime.objects.get(movie_id=movie)   
            seat_object = Seat.objects.filter(  showtime_id = showtime_object, 
                                            seat_id = i).update(is_available = False)
            response = {"seat_ticket": i,
                        "showtime": showtime_object.showtime }
            array_seat.append(response)
        
        return Response(array_seat)
        



