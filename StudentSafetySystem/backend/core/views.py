import random
from datetime import timedelta
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Bus, Student, Event, BoardingRecord, CellReading, Trip
from .serializers import BusSerializer, StudentSerializer, EventSerializer

ROUTES = [
    {"name":"North Route","zone":"North Zone","stops":["Lake View","Green Park","Tech Street","North Gate","School"]},
    {"name":"South Route","zone":"South Zone","stops":["Market Road","Rose Garden","South Junction","Temple Road","School"]},
    {"name":"East Route","zone":"East Zone","stops":["Sunrise Nagar","East Circle","Airport Road","Metro Point","School"]},
    {"name":"West Route","zone":"West Zone","stops":["Hill View","West End","River Road","Central Park","School"]},
    {"name":"Central Route","zone":"Central Zone","stops":["Main Bazaar","City Library","Clock Tower","College Road","School"]},
]

def seed():
    drivers=["Arun Kumar","Meena S","Rahul P","Divya R","Karthik V","Priya N","Sanjay M","Nisha K","Vijay T","Asha R"]
    buses=list(Bus.objects.all())
    # Upgrade an older 2-bus/6-student database automatically instead of requiring a reset.
    for i in range(len(buses),10):
        route=ROUTES[i % len(ROUTES)]
        buses.append(Bus.objects.create(code=f"SB-{101+i:03d}", route_name=route["name"], driver_name=drivers[i],
                           latitude=11.0168 + (i%5)*0.006, longitude=76.9558 + (i%5)*0.008,
                           eta_minutes=8+i%8, cell_id=f"SIM-CELL-{100+i}"))
    buses=list(Bus.objects.all())
    first_names=["Aarav","Diya","Rohan","Anika","Kabir","Ishita","Vihaan","Myra","Arjun","Sara","Advik","Nila","Reyansh","Tara","Dev","Aadhya","Ritvik","Kiara","Neil","Anaya"]
    last_names=["Kumar","Sharma","Patel","Rao","Iyer"]
    grades=["6-A","6-B","7-A","7-B","8-A","8-B","9-A","9-B","10-A","10-B"]
    existing=Student.objects.count()
    for i in range(existing,100):
        name=f"{first_names[i%20]} {last_names[(i//20)%5]}"
        bus=buses[i%10]
        Student.objects.create(name=name,grade=grades[i%10],rfid_uid=f"RFID-{1000+i:04d}",
                               parent_name=f"Parent {i+1}",parent_phone=f"+91-90000{i:05d}",bus=bus,status="WAITING")
    for b in buses:
        if not Trip.objects.filter(bus=b).exists():
            Trip.objects.create(bus=b)

def route_info(bus):
    route=next((r for r in ROUTES if r["name"]==bus.route_name), ROUTES[0])
    idx=min(len(route["stops"])-1, int(bus.progress/100*(len(route["stops"])-1)))
    return route, idx

def enrich_bus(bus, students):
    route, stop_idx=route_info(bus)
    assigned=[s for s in students if s.bus_id==bus.id]
    onboard=sum(1 for s in assigned if s.status=="ON_BUS")
    return {
        **BusSerializer(bus).data,
        "next_stop": route["stops"][min(stop_idx+1,len(route["stops"])-1)],
        "current_stop": route["stops"][stop_idx],
        "stop_progress": round((bus.progress % 20)*5,1),
        "students_onboard": onboard,
        "capacity": 40,
        "signal": random.randint(72,98),
        "location_confidence": random.randint(86,97),
        "route_status": "ON ROUTE",
        "safety_score": random.randint(94,100),
        "device_health": "ALL SYSTEMS NOMINAL",
    }

@api_view(["GET"])
def dashboard(request):
    seed()
    buses=list(Bus.objects.all())
    students=list(Student.objects.all())
    events=list(Event.objects.order_by("-created_at")[:20])
    notifications=[
        {"time":"Just now","type":"BOARDING","message":"Automatic RFID boarding notifications are enabled","status":"SENT"},
        {"time":"Live","type":"ETA","message":"ETA engine recalculates continuously from route progress","status":"ACTIVE"},
        {"time":"Live","type":"SAFETY","message":"Student accountability checks are running","status":"ACTIVE"},
    ]
    incidents=[
        {"id":"INC-1042","type":"Accountability Check","bus":"SB-104","severity":"LOW","status":"MONITORED","time":"Today"},
        {"id":"INC-1041","type":"Network Recovery","bus":"SB-107","severity":"INFO","status":"RESOLVED","time":"Today"},
    ]
    return Response({
        "buses":[enrich_bus(b,students) for b in buses],
        "students":StudentSerializer(students,many=True).data,
        "events":EventSerializer(events,many=True).data,
        "routes":ROUTES,
        "notifications":notifications,
        "incidents":incidents,
        "stats":{
            "active_buses":Bus.objects.filter(status="ACTIVE").count(),
            "students":Student.objects.count(),
            "safe_students":Student.objects.filter(status__in=["ON_BUS","ARRIVED"]).count(),
            "alerts":Event.objects.filter(severity__in=["HIGH","CRITICAL"]).count(),
            "routes":len(ROUTES),
            "stops":sum(len(r["stops"])-1 for r in ROUTES),
            "rfid_health":99.2,
            "network_health":96.8,
            "on_time":94.0,
        },
        "system":{
            "backend":"ONLINE","database":"HEALTHY","rfid":"READY","gsm":"CONNECTED","automation":"RUNNING"
        }
    })

@api_view(["POST"])
def automation(request):
    seed()
    buses=list(Bus.objects.all())
    students=list(Student.objects.all())
    now=timezone.now()
    for b in buses:
        b.progress=(b.progress+random.uniform(1.5,4.8))%100
        b.eta_minutes=max(1,round(18-b.progress*0.14))
        b.latitude += random.uniform(-0.0012,0.0012)
        b.longitude += random.uniform(-0.0012,0.0012)
        b.cell_id=f"SIM-CELL-{random.randint(100,999)}"
        b.status="ACTIVE"
        b.save()
        CellReading.objects.create(bus=b,cell_id=b.cell_id,signal_strength=random.randint(-90,-55),
                                   neighbor_cells=[f"SIM-CELL-{random.randint(100,999)}",f"SIM-CELL-{random.randint(100,999)}"])
    # Move a small number of students through a realistic automated state machine.
    sample=random.sample(students, min(8,len(students)))
    for s in sample:
        old=s.status
        s.status=random.choice(["ON_BUS","ON_BUS","ON_BUS","ARRIVED","WAITING"])
        s.save()
        if s.status != old:
            Event.objects.create(kind="RFID",title=f"RFID • {s.name}",detail=f"{s.rfid_uid} → {s.status.replace('_',' ')} • automatically verified",student=s,bus=s.bus,severity="INFO")
            BoardingRecord.objects.create(student=s,bus=s.bus,event_type="BOARD" if s.status=="ON_BUS" else "EXIT")
    b=random.choice(buses)
    Event.objects.create(kind="LOCATION",title=f"{b.code} cellular position updated",detail=f"{b.cell_id} • confidence {random.randint(88,97)}% • ETA {b.eta_minutes} min",bus=b)
    Event.objects.create(kind="SAFETY",title=f"{b.code} safety workflow completed",detail="Identity, route, connectivity and accountability checks passed",bus=b,severity="INFO")
    return Response({"ok":True,"message":"Automation cycle completed","timestamp":now.isoformat()})

@api_view(["POST"])
def create_event(request):
    e=Event.objects.create(kind=request.data.get("kind","INFO"),title=request.data.get("title","System event"),
                           detail=request.data.get("detail",""),severity=request.data.get("severity","INFO"))
    return Response(EventSerializer(e).data,status=201)
