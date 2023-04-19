from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Seat, Showtime
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from decouple import config
import requests
import json

MOVIE_PATH = config("MOVIE_PATH")
TICKET_PATH = config("TICKET_PATH")

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

        # GET moviel detail, title and cinema
        movie_detail = requests.get(f"{MOVIE_PATH}movies_service/movies/{movie_id}").json()

        array_seat = []
        for i in data["seat_id"]:
            showtime_object = Showtime.objects.get(id=showtime_id, movie_id=movie_id)
            seat_object = Seat.objects.filter(  showtime_id = showtime_object, 
                                            seat_id = i).update(is_available = False)
            response = {"seat_ticket": i,
                        "showtime": showtime_object.showtime }
            array_seat.append(response)

        # POST to create ticket
        data = {"title" : movie_detail["title"],
                "seat_number" : data["seat_id"], 
                "cinema" : movie_detail["cinema"], 
                "showtime" : str(showtime_object.showtime)}
        headers = {'Content-type': 'application/json'}
        ticket_list = requests.post(    f"{TICKET_PATH}ticket_service/create-ticket", 
                                        data=json.dumps(data),
                                        headers=headers
                                                                                    )  
        return Response(ticket_list.json())


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