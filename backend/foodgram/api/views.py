from api.filters import IngredientSearchFilter, RecipeFilterSet
from api.pagination import PageNumberLimitPagination
from api.permissions import AuthorAdminOrReadOnly, IsAdminOrReadOnly
from api.serializers import (CustomUserSerializer, FollowSerializer,
                             IngredientSerializer,
                             RecipeCreateUpdateSerializer, RecipeSerializer,
                             ShortRecipeSerializer, TagSerializer)
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from recipes.models import (Cart, Favorite, Ingredient, IngredientInRecipe,
                            Recipe, Tag)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import Follow

User = get_user_model()

SELFSUBSCRIPTION = 'Вы не можете подписываться на самого себя'
SUBSCRIBED_ALREADY = 'Вы уже подписаны на данного пользователя'
SELFUNSUBSCRIPTION = 'Вы не можете отписываться от самого себя'
UNSUBSCRIBED_ALREADY = 'Вы уже отписались'
RECIPE_IN_FAVORITES = 'Рецепт уже добавлен в список'
RECIPE_REMOVED = 'Рецепт уже удален'
PDF_HEADER = 'Список ингредиентов'


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'
    pagination_class = PageNumberLimitPagination

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            if user == author:
                return Response({
                    'errors': SELFSUBSCRIPTION
                }, status=status.HTTP_400_BAD_REQUEST)
            if Follow.objects.filter(user=user, author=author).exists():
                return Response({
                    'errors': SUBSCRIBED_ALREADY
                }, status=status.HTTP_400_BAD_REQUEST)

            follow = Follow.objects.create(user=user, author=author)
            serializer = FollowSerializer(
                follow, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if user == author:
                return Response({
                    'errors': SELFUNSUBSCRIPTION
                }, status=status.HTTP_400_BAD_REQUEST)
            follow = Follow.objects.filter(user=user, author=author)
            if follow.exists():
                follow.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

            return Response({
                'errors': UNSUBSCRIBED_ALREADY
            }, status=status.HTTP_400_BAD_REQUEST)
        return 'forbidden method'

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = PageNumberLimitPagination
    filterset_class = RecipeFilterSet
    permission_classes = (AuthorAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return RecipeCreateUpdateSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            return self.add_recipe(Favorite, request.user, pk)
        elif request.method == 'DELETE':
            return self.delete_recipe(Favorite, request.user, pk)
        return None

    def add_recipe(self, model, user, recipe_id):
        if model.objects.filter(user=user, recipe__id=recipe_id).exists():
            return Response({
                'errors': RECIPE_IN_FAVORITES
            }, status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=recipe_id)
        model.objects.create(user=user, recipe=recipe)
        serializer = ShortRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_recipe(self, model, user, recipe__id):
        obj = model.objects.filter(user=user, recipe__id=recipe__id)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({
            'errors': RECIPE_REMOVED
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            return self.add_recipe(Cart, request.user, pk)
        elif request.method == 'DELETE':
            return self.delete_recipe(Cart, request.user, pk)
        return None

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients = IngredientInRecipe.objects.filter(
            recipe__cart__user=request.user).values_list(
            'ingredient__name', 'ingredient__measurement_unit',
            'amount')
        counted_ingredients = ingredients.values(
            'ingredient__name', 'ingredient__measurement_unit').annotate(
            total=Sum('amount'))
        pdfmetrics.registerFont(
            TTFont('Montserrat', 'Montserrat.ttf', 'UTF-8'))
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_list.pdf"')
        page = canvas.Canvas(response)
        page.setFont('Montserrat', size=24)
        page.drawCentredString(200, 800, PDF_HEADER)
        page.setFont('Montserrat', size=16)
        height = 750
        for ingredient in counted_ingredients:
            page.drawString(75, height, (
                f'{ingredient["ingredient__name"]} - {ingredient["total"]}, '
                f'{ingredient["ingredient__measurement_unit"]}'
            ))
            height -= 25
        page.showPage()
        page.save()
        return response


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None
