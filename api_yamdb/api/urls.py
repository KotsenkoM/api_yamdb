from django.urls import include, path
from rest_framework import routers

from .views import (TitleViewSet, GenreViewSet, CategoryViewSet,
                    UserViewSet, signup, get_auth_token,
                    )

router_v1 = routers.DefaultRouter()
router_v1.register(r'categories', CategoryViewSet, basename='category')
router_v1.register(r'genres', GenreViewSet, basename='genre')
router_v1.register(r'titles', TitleViewSet, basename='title')
router_v1.register(r'users', UserViewSet)

v1_patterns = [
    path('', include(router_v1.urls)),
]

urlpatterns = [
    path('v1/auth/token/', get_auth_token),
    path('v1/auth/signup/', signup),
    path('v1/', include(router_v1.urls)),
]

