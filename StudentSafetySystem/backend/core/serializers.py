from rest_framework import serializers
from .models import Bus, Student, Event, BoardingRecord, CellReading, Trip

class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = "__all__"

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

class BoardingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardingRecord
        fields = "__all__"

class CellSerializer(serializers.ModelSerializer):
    class Meta:
        model = CellReading
        fields = "__all__"

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = "__all__"
