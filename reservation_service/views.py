from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Seat, Showtime
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.utils import dateformat, dateparse

@api_view(['GET', 'POST'])
def get_seat(request, movie_id, showtime_id):
    if request.method == 'GET':
        try:
            showtime_object = Showtime.objects.get(id=showtime_id, movie_id=movie_id)
            seat_object = Seat.objects.filter(showtime_id=showtime_object)
            # While GET request should not create a resource, it is for development only.
            # We will need to fix it later.
            if not seat_object:
                for i in range(10):
                    Seat.objects.create(showtime_id=showtime_object,
                                        seat_id=i + 1,
                                        is_available=True)
            array_seat = []
            for i in range(len(seat_object)):
                array_seat.append({"seat_id": seat_object[i].seat_id,
                                   "is_available": seat_object[i].is_available

                                   })
            return Response(array_seat)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND) 

    elif request.method == 'POST':
        data = request.data
        for i in data["seat_id"]:
            showtime_object = Showtime.objects.get(id=showtime_id, movie_id=movie_id)
            seat_object = Seat.objects.get(  showtime_id = showtime_object, 
                                            seat_id = i)
            if seat_object.is_available == False:
                return Response("Fail to reserve")
        
        array_seat = []
        for i in data["seat_id"]:
            showtime_object = Showtime.objects.get(id=showtime_id, movie_id=movie_id)
            seat_object = Seat.objects.filter(  showtime_id = showtime_object, 
                                            seat_id = i).update(is_available = False)
            response = {"seat_ticket": i,
                        "showtime": showtime_object.showtime }
            array_seat.append(response)
        
        return Response(array_seat)


@api_view(['GET'])
def get_all_showtimes(request, movie_id):
    if not Showtime.objects.filter(movie_id=movie_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    showtimes = Showtime.objects.filter(movie_id=movie_id).order_by('showtime')
    showtimes_list = []
    for showtime in showtimes:
        showtimes_list.append({
            'showtime_id': showtime.id,
            'start_time': showtime.showtime
        })
    return Response(showtimes_list)


@api_view(['POST'])
def initialize_reservation(request, movie_id):
    if Showtime.objects.filter(movie_id=movie_id).exists():
        return Response({
            "message": "Movie already exists.",
            "code": "movie_exists"
        }, status=400) # Bad Request
    start_time = dateparse.parse_datetime(request.data['showtime'])
    showtime_object = Showtime.objects.create(movie_id=movie_id, showtime=start_time)
    # TODO: Validate request (amount must be a positive number)
    amount = request.data['amount']
    for i in range(amount):
        Seat.objects.create(seat_id=i+1, showtime_id=showtime_object)
    return Response(status=204)