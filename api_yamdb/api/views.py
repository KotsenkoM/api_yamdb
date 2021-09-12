from django.db.models import Avg
from django_filters import FilterSet, CharFilter, NumberFilter
from reviews.models import Title, Genre, Category
from rest_framework import viewsets, filters, mixins

from .permissions import IsAdminOrReadOnly, ReviewCommentPermission, IsAdmin
from .serializers import (
    TitleSerializer,
    GenreSerializer,
    CategorySerializer,
    TitleUpdateCreateSerializer,
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
