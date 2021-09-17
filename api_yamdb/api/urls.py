from django.urls import include, path

from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet, get_auth_token,
                    signup)

router_v1 = routers.DefaultRouter()
router_v1.register(r'categories', CategoryViewSet, basename='category')
router_v1.register(r'genres', GenreViewSet, basename='genre')
router_v1.register(r'titles', TitleViewSet, basename='title')
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)
router_v1.register(r'users', UserViewSet)

v1_patterns = [
    path('', include(router_v1.urls)),
]

urlpatterns = [
    path('v1/auth/token/', get_auth_token, name='token'),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/', include(router_v1.urls)),
]
