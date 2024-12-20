from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookRequestViewSet

router = DefaultRouter()
router.register('requests', BookRequestViewSet, basename='book-request')

urlpatterns = [
    path('', include(router.urls)),
]
