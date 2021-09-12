from django.urls import include, path
from rest_framework import routers

from .views import TitleViewSet, GenreViewSet, CategoryViewSet

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'titles', TitleViewSet, basename='title')

router_v1 = routers.DefaultRouter()
router_v1.register(r'users', UserViewSet)

v1_patterns = [
    path('', include(router_v1.urls)),
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include(v1_patterns)),
    path('v1/auth/signup/', signup)
]
