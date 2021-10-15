from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from game.serializers import GameViewSet

router = routers.DefaultRouter()
router.register("", GameViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
]
