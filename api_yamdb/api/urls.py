from rest_framework import routers
from rest_framework.authtoken import views
from django.urls import include, path

from .views import UserViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'users', UserViewSet)

v1_patterns = [
    path('', include(router_v1.urls)),
    path('auth/', views.obtain_auth_token),
]

urlpatterns = [
    path('v1/', include(v1_patterns)),
]