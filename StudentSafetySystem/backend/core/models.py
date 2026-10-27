from django.db import models

class Bus(models.Model):
    code=models.CharField(max_length=30, unique=True)
    route_name=models.CharField(max_length=120)
    driver_name=models.CharField(max_length=120, blank=True)
    status=models.CharField(max_length=30, default="ACTIVE")
    latitude=models.FloatField(default=11.0168)
    longitude=models.FloatField(default=76.9558)
    progress=models.FloatField(default=0)
    eta_minutes=models.IntegerField(default=12)
    cell_id=models.CharField(max_length=80, default="SIM-CELL-001")
    updated_at=models.DateTimeField(auto_now=True)

class Student(models.Model):
    name=models.CharField(max_length=120)
    grade=models.CharField(max_length=40)
    rfid_uid=models.CharField(max_length=80, unique=True)
    parent_name=models.CharField(max_length=120)
    parent_phone=models.CharField(max_length=30, blank=True)
    bus=models.ForeignKey(Bus, on_delete=models.SET_NULL, null=True, blank=True)
    status=models.CharField(max_length=30, default="WAITING")

class Trip(models.Model):
    bus=models.ForeignKey(Bus,on_delete=models.CASCADE)
    status=models.CharField(max_length=30,default="RUNNING")
    started_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Event(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    kind=models.CharField(max_length=40)
    title=models.CharField(max_length=200)
    detail=models.TextField(blank=True)
    severity=models.CharField(max_length=20,default="INFO")
    bus=models.ForeignKey(Bus,on_delete=models.SET_NULL,null=True,blank=True)
    student=models.ForeignKey(Student,on_delete=models.SET_NULL,null=True,blank=True)

class BoardingRecord(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    bus=models.ForeignKey(Bus,on_delete=models.CASCADE)
    event_type=models.CharField(max_length=20,default="BOARD")
    created_at=models.DateTimeField(auto_now_add=True)
    source=models.CharField(max_length=30,default="RFID")

class CellReading(models.Model):
    bus=models.ForeignKey(Bus,on_delete=models.CASCADE)
    cell_id=models.CharField(max_length=80)
    signal_strength=models.IntegerField(default=-72)
    neighbor_cells=models.JSONField(default=list)
    created_at=models.DateTimeField(auto_now_add=True)
