from rest_framework import serializers


class ReservationCreation(serializers.Serializer):
    amount_of_seats = serializers.IntegerField(min_value=1)
    start_time = serializers.DateTimeField()
