from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import (RecipeSerializer, TagSerializer,
                          IngredientSerializer, UserSerializer)
from recipes.models import Recipe, Tag, Ingredient
from users.models import User


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # permission_classes = (AdminOnly,)
    lookup_field = 'id'
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    # filterset_class = RecipeFilter
    # filterset_fields = ('is_favorited', 'author', 'is_in_shopping_cart',
    #                     'tags')
    # permission_classes = (AuthorAdminModeratorOrReadOnly,)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('name',)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
