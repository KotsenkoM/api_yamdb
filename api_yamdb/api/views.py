from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import permissions
from django.db.models import Avg
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator


from users.models import User
from .mixins import CustomViewSet
from .serializers import UserSerializer
from .filters import TitlesFilter
from reviews.models import Title, Genre, Category, Review
from rest_framework import viewsets, filters

from .permissions import IsAdminOrReadOnly, IsAdmin, ReviewCommentPermission
from .serializers import (
    TitleSerializer,
    GenreSerializer,
    CategorySerializer,
    TitleUpdateCreateSerializer,
    RegistrationSerializer,
    LoginSerializer,
    EmailSerializer,
    ConfirmationSerializer,
    ReviewSerializer
)


class CategoryViewSet(CustomViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CustomViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = TitlesFilter
    http_method_names = ['get', 'post', 'delete', 'patch']

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update', 'destroy']:
            return TitleUpdateCreateSerializer
        return TitleSerializer


@api_view(['POST'])
def signup(request):
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    user, create = User.objects.get_or_create(email=email, username=username)
    confirmation_code = default_token_generator.make_token(user)
    send_mail('cod', f'Ваш код подтверждения {confirmation_code}',
              settings.DEFAULT_FROM_EMAIL, [email])
    return Response({'email': email, 'username': username})


@api_view(['POST'])
def get_auth_token(request):
    serializer = ConfirmationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    confirmation_code = serializer.validated_data['confirmation_code']
    user = get_object_or_404(
        User,
        username=username,
    )
    if default_token_generator.check_token(user, confirmation_code):
        user.is_active = True
        user.save()
        token = AccessToken.for_user(user)
        return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
    return Response('Неверный код подтверждения',
                    status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (permissions.IsAuthenticated, IsAdmin,)

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request):
        serializer = UserSerializer(
            self.request.user,
            data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
