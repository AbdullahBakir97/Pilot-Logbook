from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AircraftViewSet, FlightLogViewSet

router = DefaultRouter()
router.register(r'aircraft', AircraftViewSet)
router.register(r'flightlogs', FlightLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
