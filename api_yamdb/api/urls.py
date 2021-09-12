from django.urls import include, path
from rest_framework import routers

from .views import TitleViewSet, GenreViewSet, CategoryViewSet

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'titles', TitleViewSet, basename='title')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', signup)
]
