from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.permissions import IsAdminOrReadOnly
from api.serializers import (RecipeSerializer, TagSerializer,
                          IngredientSerializer, UserSerializer)
from recipes.models import Recipe, Tag, Ingredient
from users.models import User

from djoser.views import UserViewSet as DjoserUserViewSet


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    # filterset_class = RecipeFilter
    # filterset_fields = ('is_favorited', 'author', 'is_in_shopping_cart',
    #                     'tags')
    # permission_classes = (AuthorAdminModeratorOrReadOnly,)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None
