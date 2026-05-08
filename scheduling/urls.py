from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScheduleViewSet, MallViewSet

router = DefaultRouter()
router.register(r'malls',     MallViewSet,     basename='mall')
router.register(r'schedules', ScheduleViewSet, basename='schedule')

urlpatterns = [
    path('', include(router.urls)),
]