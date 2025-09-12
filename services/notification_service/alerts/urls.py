from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlertViewSet, health, me

router = DefaultRouter()
router.register(r"alerts", AlertViewSet, basename="alert")

urlpatterns = [
    path("health/", health, name="health"),
    path("me/", me, name="me"),
    path("", include(router.urls)),
]