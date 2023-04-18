from rest_framework import serializers


class ReservationInitSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)
    showtime = serializers.DateTimeField()
