from django.urls import path
from .views import dashboard, automation, create_event
urlpatterns=[
    path("dashboard/",dashboard),
    path("automation/cycle/",automation),
    path("events/",create_event),
]
