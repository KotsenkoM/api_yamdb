from rest_framework import routers
from django.urls import include, path

from .views import UserViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'users', UserViewSet)

v1_patterns = [
    path('', include(router_v1.urls)),
]

urlpatterns = [
    path('v1/', include(v1_patterns)),
]