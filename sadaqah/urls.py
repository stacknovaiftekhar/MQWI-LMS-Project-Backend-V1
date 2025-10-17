from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PurposeViewSet, SadaqahViewSet

router = DefaultRouter()
router.register(r'purpose', PurposeViewSet)
router.register(r'sadaqah', SadaqahViewSet)

urlpatterns = [
    path('', include(router.urls)),
]