from django.contrib import admin
from .models import Bus, Student, Trip, Event, BoardingRecord, CellReading
admin.site.register([Bus,Student,Trip,Event,BoardingRecord,CellReading])
