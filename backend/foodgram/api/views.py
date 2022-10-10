from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from api.permissions import IsAdminOrReadOnly
from api.serializers import (RecipeSerializer, RecipeCreateSerializer, TagSerializer,
                          IngredientSerializer, UserSerializer)
from recipes.models import Recipe, Tag, Ingredient, IngredientInRecipe
from users.models import User


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

    def create_ingredients_in_recipe(self, recipe, ingredients):
        for ingredient in ingredients:
            # for key, value in ingredient:
            #     print(f'{key}, {value}')  # потом убрать!
            # print(ingredient)
            # print(ingredients)
            IngredientInRecipe.objects.create(
                ingredient=Ingredient.objects.get(id=ingredient['id']),
                recipe=recipe,
                amount=ingredient['amount']
            )

    def create_tags_in_recipe(self, recipe, tags):
        for tag in tags:
            recipe.tags.set([Tag.objects.get(id=tag)])

    def create(self, request, *args, **kwargs):
        serializer = RecipeCreateSerializer(
            data=self.request.data,
            context={'request': self.request}
        )
        print(f'request data: {self.request.data}')
        if serializer.is_valid(raise_exception=True):
            print(f'serializer data: {serializer.data}')
            print(f'serializer validated data: {serializer.validated_data}')
            ingredients = serializer.validated_data.pop('ingredients')
            tags = serializer.validated_data.pop('tags')
            recipe = Recipe.objects.create(author=self.request.user, **serializer.validated_data)
            self.create_ingredients_in_recipe(recipe=recipe, ingredients=ingredients)
            self.create_tags_in_recipe(recipe=recipe, tags=tags)
            serializer = RecipeSerializer(
                instance=recipe,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
