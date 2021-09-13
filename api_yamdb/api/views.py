from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions


from users.models import User
from .serializers import UserSerializer
from django_filters import FilterSet, CharFilter, NumberFilter
from reviews.models import Title, Genre, Category
from rest_framework import viewsets, filters, mixins

from .permissions import IsAdminOrReadOnly, IsAdmin
from .serializers import (
    TitleSerializer,
    GenreSerializer,
    CategorySerializer,
    TitleUpdateCreateSerializer,
    RegistrationSerializer,
    LoginSerializer,
)


class CustomViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                    mixins.DestroyModelMixin, viewsets.GenericViewSet):
    pass


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


class TitlesFilter(FilterSet):
    category = CharFilter(
        field_name='category__slug',
        lookup_expr='iexact'
    )
    genre = CharFilter(
        field_name='genre__slug',
        lookup_expr='iexact'
    )
    name = CharFilter(
        field_name='name',
        lookup_expr='contains'
    )
    year = NumberFilter(
        field_name='year',
        lookup_expr='iexact'
    )

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()#.annotate(rating=Avg('reviews__score'))
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = TitlesFilter
    http_method_names = ['get', 'post', 'delete', 'patch']

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update', 'destroy']:
            return TitleUpdateCreateSerializer
        return TitleSerializer


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def get_auth_token(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    confirmation_code = serializer.validated_data['confirmation_code']
    user = get_object_or_404(
        User,
        email=email,
        confirmation_code=confirmation_code,
    )
    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)
    return Response({'token': token})


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
